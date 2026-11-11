(function(){let e=null,t=e=>self.postMessage(e);self.onmessage=async({data:n})=>{if(n.type===`initialize`)try{let{loadPyodide:r}=await import(
/* @vite-ignore */
`${n.indexURL}pyodide.mjs`);if(e=await r({indexURL:n.indexURL}),!e)throw Error(`Runtime initialization failed`);e.FS.writeFile(`/home/pyodide/workshop_support.py`,`"""Portable execution helpers for the workshop's formative checks.

These run Python in the current interpreter, with fresh script globals and
controlled streams. The browser supervises the worker's execution deadline.
They deliberately do not emulate subprocesses or pretend to isolate hostile code.
"""
import builtins
import contextlib
import io
import os
import runpy
import sys
import traceback
from types import SimpleNamespace

OUTPUT_LIMIT = 100_000


class LimitedOutput(io.StringIO):
    """Bound stored output even when a learner accidentally prints in a loop."""
    def __init__(self):
        super().__init__()
        self.truncated = False

    def write(self, value):
        remaining = max(0, OUTPUT_LIMIT - self.tell())
        super().write(value[:remaining])
        self.truncated = self.truncated or len(value) > remaining
        return len(value)

    def display_value(self):
        suffix = "\\n[Output truncated after 100,000 characters.]" if self.truncated else ""
        return self.getvalue() + suffix


def _execute(action, input_text="", argv=None, before_input=None):
    output, errors = LimitedOutput(), LimitedOutput()
    saved_stdin, saved_argv = sys.stdin, sys.argv
    saved_profile, saved_trace = sys.getprofile(), sys.gettrace()
    builtin_namespace = vars(builtins)
    saved_builtins = dict(builtin_namespace)
    saved_path, saved_directory = list(sys.path), os.getcwd()
    returncode = 0
    try:
        sys.stdin = io.StringIO(input_text)
        sys.argv = list(argv or ["main.py"])
        if before_input is not None:
            original_input = builtins.input

            def observed_input(prompt=""):
                before_input(output.getvalue())
                return original_input(prompt)

            builtins.input = observed_input
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            try:
                action()
            except SystemExit as error:
                returncode = error.code if isinstance(error.code, int) else (0 if error.code is None else 1)
                if error.code is not None and not isinstance(error.code, int):
                    print(error.code, file=sys.stderr)
            except BaseException:
                returncode = 1
                traceback.print_exc()
    finally:
        sys.setprofile(saved_profile)
        sys.settrace(saved_trace)
        sys.stdin, sys.argv = saved_stdin, saved_argv
        sys.path[:] = saved_path
        os.chdir(saved_directory)
        builtin_namespace.clear()
        builtin_namespace.update(saved_builtins)
    return SimpleNamespace(returncode=returncode, stdout=output.display_value(), stderr=errors.display_value())


def run_script(path, input="", *, before_input=None):
    """Execute a learner script with CPython's usual __main__ semantics."""
    path = os.path.abspath(path)
    # Local imports must see current source, even after another test ran it.
    directory = os.path.dirname(path) + os.sep
    for name, module in list(sys.modules.items()):
        if str(getattr(module, "__file__", "")).startswith(directory):
            del sys.modules[name]
    return _execute(lambda: runpy.run_path(path, run_name="__main__"), input, [path], before_input)


def run_code(source, *, input="", argv=()):
    """Run a check-owned observation script, e.g. to inspect final list values."""
    namespace = {"__name__": "__main__", "__file__": "<observation>"}
    return _execute(lambda: exec(compile(source, "<observation>", "exec"), namespace), input, ["-c", *argv])


@contextlib.contextmanager
def time_limit():
    """The parent browser terminates the entire worker after ten seconds."""
    yield
`),await e.runPythonAsync(`"""Entry point shared by the browser worker and the Node verification command."""
import builtins
import contextlib
import importlib
import importlib.util
import json
import os
import shutil
import sys
import traceback
import unittest

from workshop_support import LimitedOutput, run_script

WORK_DIRECTORY = "/home/pyodide/workshop-exercise"


class WorkshopResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.details = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.details.append({"name": test.id().split(".", 1)[-1], "passed": True, "message": "Passed"})

    def _failure(self, test, error):
        # Keep the assertion's useful message and Python source traceback.
        message = "".join(traceback.format_exception(*error))[-12_000:]
        self.details.append({"name": test.id().split(".", 1)[-1], "passed": False, "message": message})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self._failure(test, error)

    def addError(self, test, error):
        super().addError(test, error)
        self._failure(test, error)

    def addSubTest(self, test, subtest, error):
        super().addSubTest(test, subtest, error)
        if error is not None:
            self._failure(subtest, error)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.details.append({"name": test.id(), "passed": False, "message": "Skipped: " + reason})


def workshop_execute(code, input_text, tests=None):
    saved_directory, saved_path = os.getcwd(), list(sys.path)
    saved_streams = (sys.stdin, sys.stdout, sys.stderr)
    builtin_namespace = vars(builtins)
    saved_builtins = dict(builtin_namespace)
    saved_profile, saved_trace = sys.getprofile(), sys.gettrace()
    output, errors = LimitedOutput(), LimitedOutput()
    result = {"stdout": "", "stderr": ""}
    try:
        for name, module in list(sys.modules.items()):
            if str(getattr(module, "__file__", "")).startswith(WORK_DIRECTORY + "/"):
                del sys.modules[name]
        shutil.rmtree(WORK_DIRECTORY, ignore_errors=True)
        os.makedirs(WORK_DIRECTORY)
        os.chdir(WORK_DIRECTORY)
        sys.path.insert(0, WORK_DIRECTORY)
        importlib.invalidate_caches()
        with open("main.py", "w", encoding="utf-8") as handle:
            handle.write(code)
        if tests is None:
            execution = run_script("main.py", input=input_text)
            result.update(stdout=execution.stdout, stderr=execution.stderr)
            if execution.returncode != 0:
                result["error"] = "The program ended with an error."
                if "EOFError" in execution.stderr:
                    result["error"] = "The program requested more input. Add one line per answer to Program input, then run again."
        else:
            with open("tests.py", "w", encoding="utf-8") as handle:
                handle.write(tests)
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                spec = importlib.util.spec_from_file_location("workshop_checks", os.path.join(WORK_DIRECTORY, "tests.py"))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                suite = unittest.defaultTestLoader.loadTestsFromModule(module)
                checks = WorkshopResult()
                suite.run(checks)
            result.update(stdout=output.display_value(), stderr=errors.display_value(), tests=checks.details,
                          passed=checks.wasSuccessful() and checks.testsRun > 0 and not checks.skipped)
            if checks.testsRun == 0:
                result["error"] = "No tests were found. Add unittest test methods to tests.py."
    except BaseException:
        result.update(stdout=output.display_value(), stderr=errors.display_value() + traceback.format_exc(),
                      error="The checks could not complete. Review the Python error below.")
    finally:
        sys.setprofile(saved_profile)
        sys.settrace(saved_trace)
        sys.stdin, sys.stdout, sys.stderr = saved_streams
        sys.path[:] = saved_path
        os.chdir(saved_directory)
        builtin_namespace.clear()
        builtin_namespace.update(saved_builtins)
    return json.dumps(result)
`),t({type:`ready`})}catch(e){t({type:`initialization-error`,error:String(e)})}else if(e)try{let r=e.globals.get(`workshop_execute`);try{let e=JSON.parse(n.tests===void 0?r(n.code,n.input):r(n.code,n.input,n.tests));t({type:`result`,id:n.id,result:e})}finally{r.destroy()}}catch(e){t({type:`result`,id:n.id,result:{stdout:``,stderr:``,error:String(e)}})}}})();
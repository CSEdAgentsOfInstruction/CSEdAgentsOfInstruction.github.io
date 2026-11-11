"""Entry point shared by the browser worker and the Node verification command."""
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

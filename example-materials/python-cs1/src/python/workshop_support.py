"""Portable execution helpers for the workshop's formative checks.

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
        suffix = "\n[Output truncated after 100,000 characters.]" if self.truncated else ""
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

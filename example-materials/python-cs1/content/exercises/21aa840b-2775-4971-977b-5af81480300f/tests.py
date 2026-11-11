# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script, time_limit
import contextlib
import importlib.util
import io
import os
import sys
import unittest
from unittest.mock import Mock, patch


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")





class BehaviorTest(unittest.TestCase):
    FUNCTIONS = ()
    LOAD_INPUTS = ()
    ALLOW_STARTUP_OUTPUT = False

    def setUp(self):
        spec = importlib.util.spec_from_file_location("student_solution", SCRIPT_PATH)
        self.module = importlib.util.module_from_spec(spec)
        output = io.StringIO()
        with time_limit(), patch("builtins.input", side_effect=self.LOAD_INPUTS), contextlib.redirect_stdout(output):
            spec.loader.exec_module(self.module)
        self.startup_output = output.getvalue()
        if not self.ALLOW_STARTUP_OUTPUT:
            self.assertEqual(self.startup_output, "", "Keep displayed output in the part of the program responsible for presentation.")
        for name in self.FUNCTIONS:
            self.assertTrue(callable(getattr(self.module, name, None)), f"Define the function {name} from the handout.")

    def call(self, name, *args):
        output = io.StringIO()
        with time_limit(), contextlib.redirect_stdout(output):
            result = getattr(self.module, name)(*args)
        return result, output.getvalue()

    def calculation(self, name, *args):
        result, output = self.call(name, *args)
        self.assertEqual(output, "", f"{name} should return its result without printing.")
        return result

    def run_program(self, responses=()):
        completed = run_script(SCRIPT_PATH, input='\n'.join(responses) + ('\n' if responses else ''))
        self.assertEqual(completed.returncode, 0, "The complete program must finish successfully.\n" + completed.stderr)
        self.assertEqual(completed.stderr, "", "The program should not write errors.")
        return completed.stdout

    def run_and_observe_calls(self, names, responses=()):
        import runpy

        observed = {name: 0 for name in names}
        previous_profile = sys.getprofile()

        def observe(frame, event, arg):
            if event == "call":
                for name in names:
                    function = frame.f_globals.get(name)
                    if getattr(function, "__code__", None) is frame.f_code:
                        observed[name] += 1

        output = io.StringIO()
        try:
            sys.setprofile(observe)
            with time_limit(), patch("builtins.input", side_effect=responses), contextlib.redirect_stdout(output):
                runpy.run_path(SCRIPT_PATH, run_name="__main__")
        finally:
            sys.setprofile(previous_profile)
        return output.getvalue(), observed

    def read(self, name, responses, *args):
        reader = Mock(side_effect=responses)
        with patch("builtins.input", reader):
            result, output = self.call(name, *args)
        return result, output, reader


class TestBadgeAudit(BehaviorTest):
    FUNCTIONS = ("has_access_code", "check_access_codes")

    def test_search_returns_the_required_boolean(self):
        cases = [(["A7", "B4"], "A7", True), (["A7", "B4", "C9"], "B4", True), (["A7", "B4", "C9"], "C9", True), (["A7", "B4"], "X2", False), ([], "A7", False), (["new", "new"], "new", True), ([""], "", True), (["A7", "a70"], "a7", False), (["A"], "A7", False), ([""], "A7", False), (["A7"], "", False), ([" A7 "], "A7", False)]
        for codes, wanted, expected in cases:
            with self.subTest(codes=codes, wanted=wanted):
                original = list(codes)
                self.assertIs(self.calculation("has_access_code", codes, wanted), expected)
                self.assertEqual(codes, original)

    def test_student_checks_pass_silently(self):
        self.calculation("check_access_codes")
        self.assertEqual(self.run_program(), "")

    def test_running_the_program_executes_the_checks(self):
        output, observed = self.run_and_observe_calls({"check_access_codes"})
        self.assertGreater(observed["check_access_codes"], 0, "Keep the call that runs check_access_codes when the program starts.")
        self.assertEqual(output, "")

    def substitute_search(self, implementation):
        from inspect import signature

        call_signature = signature(self.module.has_access_code)

        def replacement(*args, **kwargs):
            arguments = call_signature.bind(*args, **kwargs)
            return implementation(*arguments.args, **arguments.kwargs)

        return patch.object(self.module, "has_access_code", replacement)

    def test_student_checks_accept_correct_searches(self):
        def correct(codes, wanted):
            return wanted in codes
        with self.substitute_search(correct):
            self.calculation("check_access_codes")

    def test_student_checks_expose_incorrect_searches(self):
        def first_only(codes, wanted):
            if codes:
                return codes[0] == wanted
            return False

        def empty_returns_none(codes, wanted):
            if codes:
                return wanted in codes
            return None

        def always_true(codes, wanted):
            return True

        def nonempty_means_found(codes, wanted):
            return len(codes) > 0

        def always_false(codes, wanted):
            return False

        faulty_searches = [
            (first_only, "Your checks did not expose a search that examines only the first code."),
            (empty_returns_none, "Your checks did not distinguish None from the required result for an empty list."),
            (always_true, "Your checks accepted a search that always returns True."),
            (always_false, "Your checks accepted a search that always returns False."),
            (nonempty_means_found, "Your checks accepted a search that returns True for every nonempty list, even when the requested code is absent."),
        ]
        for function, feedback in faulty_searches:
            with self.subTest(fault=function.__name__):
                with self.substitute_search(function):
                    with self.assertRaises(AssertionError, msg=feedback):
                        # Capture output outside assertRaises: printing cannot count as detecting a wrong result.
                        with time_limit(), contextlib.redirect_stdout(io.StringIO()):
                            self.module.check_access_codes()


if __name__ == "__main__":
    unittest.main()

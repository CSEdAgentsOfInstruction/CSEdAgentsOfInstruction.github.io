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


class TestFestival(BehaviorTest):
    FUNCTIONS = ("attendance_summary", "main")
    LOAD_INPUTS = ("",)
    ALLOW_STARTUP_OUTPUT = True

    def test_summary_for_varied_attendance(self):
        cases = [([], 100), ([7], 100), ([120, 85, 150, 90, 150], 100), ([100, 99, 101], 100), ([0, 0, 4], 0), ([5, 1, 7, 5], 5), ([3, 4], 5)]
        for attendance, minimum in cases:
            with self.subTest(attendance=attendance, minimum=minimum):
                original = list(attendance)
                result = self.calculation("attendance_summary", attendance, minimum)
                self.assertIsInstance(result, list, "Return [period count, total, busy count].")
                self.assertEqual(result, [len(attendance), sum(attendance), sum(value >= minimum for value in attendance)])
                self.assertEqual(attendance, original, "Summarizing must not change the input list.")
                result.append(999)
                self.assertEqual(attendance, original, "Return a new result list, separate from attendance.")

    def test_complete_program_preserves_the_original_behavior(self):
        for attendance in [[], [7], [100], [99, 100, 101], [120, 85, 150, 90, 150], [0, 0, 0], [8, 101, 8, 101]]:
            with self.subTest(attendance=attendance):
                entered = " ".join(str(value) for value in attendance)
                expected = f"Periods: {len(attendance)}\nTotal visitors: {sum(attendance)}\nBusy periods: {sum(value >= 100 for value in attendance)}\n"
                self.assertEqual(self.run_program([entered]), expected)

    def test_main_uses_the_returned_summary(self):
        with patch.object(self.module, "attendance_summary", autospec=True, return_value=[4, 321, 2]) as summarize:
            result, output, reader = self.read("main", ["12 30 101"])
        summarize.assert_any_call([12, 30, 101], 100)
        self.assertEqual(reader.call_count, 1)
        self.assertEqual(output, "Periods: 4\nTotal visitors: 321\nBusy periods: 2\n")

    def test_summary_calls_a_chosen_helper(self):
        from types import FunctionType

        summary = self.module.attendance_summary
        helpers_called = []
        previous_profile = sys.getprofile()

        def observe(frame, event, arg):
            if event != "call" or frame.f_globals is not self.module.__dict__:
                return
            # Observe functions executing within this summary call, including
            # helpers defined locally. Code identity identifies the running
            # function; no statements or bytecode are inspected.
            namespace = dict(frame.f_globals)
            if frame.f_back is not None:
                namespace.update(frame.f_back.f_locals)
            for function in namespace.values():
                if isinstance(function, FunctionType) and function is not summary and function.__code__ is frame.f_code:
                    helpers_called.append(function)
                    break

        try:
            sys.setprofile(observe)
            result = self.calculation("attendance_summary", [99, 100, 101], 100)
        finally:
            sys.setprofile(previous_profile)

        self.assertEqual(result, [3, 300, 2])
        self.assertTrue(helpers_called, "Choose a calculation for a helper function and call it from attendance_summary.")

    def test_program_runs_the_refactored_flow(self):
        output, observed = self.run_and_observe_calls({"main", "attendance_summary"}, ["99 100 101"])
        self.assertTrue(all(count > 0 for count in observed.values()), "Running the program should call main and use attendance_summary.")
        self.assertEqual(output, "Periods: 3\nTotal visitors: 300\nBusy periods: 2\n")

    def test_whitespace_and_integer_spellings(self):
        self.assertEqual(self.run_program(["  +0100\t000  101  "]), "Periods: 3\nTotal visitors: 201\nBusy periods: 2\n")
        self.assertEqual(self.run_program(["   \t "]), "Periods: 0\nTotal visitors: 0\nBusy periods: 0\n")


if __name__ == "__main__":
    unittest.main()

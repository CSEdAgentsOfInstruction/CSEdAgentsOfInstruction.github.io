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


class TestLaunchLevel(BehaviorTest):
    FUNCTIONS = ("read_bounded_integer", "main")
    LOAD_INPUTS = ("1",)
    ALLOW_STARTUP_OUTPUT = True

    def check_input(self, responses, minimum, maximum, expected, messages):
        result, output, reader = self.read("read_bounded_integer", responses, "Level? ", minimum, maximum)
        self.assertIs(type(result), int)
        self.assertEqual(result, expected)
        self.assertEqual(output.splitlines(), messages)
        self.assertEqual(reader.call_count, len(responses), "Stop after the first valid value.")
        self.assertTrue(all(call.args == ("Level? ",) for call in reader.call_args_list), "Use the supplied prompt on every attempt.")

    def test_retries_after_conversion_and_range_errors(self):
        self.check_input(["many", "-3", "8", "3"], 1, 5, 3, ["Please enter an integer.", "Please enter a value from 1 to 5.", "Please enter a value from 1 to 5."])

    def test_different_bounds_and_repeated_invalid_attempts(self):
        self.check_input(["", "2.5", "8", "13", "12"], 9, 12, 12, ["Please enter an integer.", "Please enter an integer.", "Please enter a value from 9 to 12.", "Please enter a value from 9 to 12."])
        self.check_input(["-6", "0", "-4"], -5, -2, -4, ["Please enter a value from -5 to -2."] * 2)

    def test_both_boundaries_and_a_single_value_range(self):
        for entered, low, high, expected in [("-2", -2, 2, -2), ("2", -2, 2, 2), ("0", 0, 0, 0), ("  +0012 ", 10, 12, 12), ("-0", 0, 5, 0)]:
            with self.subTest(entered=entered): self.check_input([entered], low, high, expected, [])

    def test_unexpected_input_failure_is_not_hidden(self):
        with patch("builtins.input", side_effect=[EOFError("input unavailable"), "3"]):
            with self.assertRaises(EOFError):
                self.call("read_bounded_integer", "", 1, 5)

    def test_program_runs_main(self):
        output, observed = self.run_and_observe_calls({"main"}, ["3"])
        self.assertGreater(observed["main"], 0, "Run the program through main so it coordinates the helper functions.")

    def test_main_uses_the_value_returned_by_the_input_helper(self):
        with patch.object(self.module, "read_bounded_integer", autospec=True, return_value=3) as read_level:
            result, output, reader = self.read("main", ["1"])
        read_level.assert_called_once_with("", 1, 5)
        self.assertEqual(reader.call_count, 0, "Let read_bounded_integer handle the input.")
        self.assertEqual(output, "Level: 3\n")

    def test_every_valid_level_in_the_complete_program(self):
        for level in range(1, 6):
            with self.subTest(level=level):
                self.assertEqual(self.run_program([str(level)]), f"Level: {level}\n")

    def test_complete_interactions(self):
        cases = [(["1"], "Level: 1\n"), (["5"], "Level: 5\n"), (["high", "-1", "0", "6", "5"], "Please enter an integer.\n" + "Please enter a value from 1 to 5.\n" * 3 + "Level: 5\n"), (["  +0004  "], "Level: 4\n")]
        for responses, expected in cases:
            with self.subTest(responses=responses): self.assertEqual(self.run_program(responses), expected)


if __name__ == "__main__":
    unittest.main()

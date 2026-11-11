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

    def read(self, name, responses, *args):
        reader = Mock(side_effect=responses)
        with patch("builtins.input", reader):
            result, output = self.call(name, *args)
        return result, output, reader


class TestNormalize(BehaviorTest):
    FUNCTIONS = ("replace_negative_readings",)

    def check_values(self, entered):
        values = list(entered)
        alias = values
        expected = [0 if value < 0 else value for value in entered]
        result = self.calculation("replace_negative_readings", values)
        self.assertIsNone(result, "Change the supplied list and return None.")
        self.assertEqual(values, expected, "Replace every negative value and leave other values in order.")
        self.assertEqual(alias, expected, "Other names for the same list must observe the changes.")

    def test_mixed_values_and_repetitions(self):
        for values in [[4, -2, 0, -7, 5], [-8, 2, -8, 2], [1.5, -0.5, 2.5]]:
            with self.subTest(values=values): self.check_values(values)

    def test_empty_single_and_no_changes(self):
        for values in [[], [-1], [0], [5], [0, 2, 8], [-1, -2, -3]]:
            with self.subTest(values=values): self.check_values(values)

    def test_repeating_a_cleanup_does_not_change_clean_values(self):
        values = [-1, 0, 4]
        self.calculation("replace_negative_readings", values)
        self.calculation("replace_negative_readings", values)
        self.assertEqual(values, [0, 0, 4])


if __name__ == "__main__":
    unittest.main()

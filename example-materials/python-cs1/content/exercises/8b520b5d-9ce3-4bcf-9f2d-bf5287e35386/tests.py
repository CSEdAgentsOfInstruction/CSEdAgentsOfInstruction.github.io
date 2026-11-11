# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script, time_limit
import contextlib
import importlib.util
import io
import math
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


class TestRouteCost(BehaviorTest):
    FUNCTIONS = ("route_cost",)

    def check_cases(self, cases):
        for distance, rate in cases:
            with self.subTest(distance=distance, rate=rate):
                result = self.calculation("route_cost", distance, rate)
                self.assertIsNotNone(result, "Return the calculated cost.")
                self.assertTrue(
                    math.isfinite(result)
                    and math.isclose(result, distance * rate, rel_tol=1e-12, abs_tol=0.0),
                    "Return the multiplication result without rounding or truncating it.",
                )

    def test_ordinary_costs(self):
        self.check_cases([(12, 1.5), (3.5, 2), (125, 0.08)])

    def test_fractional_results_are_not_truncated_or_rounded(self):
        self.check_cases([(1.5, 1.5), (7, 0.35), (0.125, 0.25), (123.45, 6.789)])

    def test_zero_in_either_argument(self):
        self.check_cases([(0, 8), (15, 0), (0, 0)])

    def test_small_and_precise_products(self):
        self.check_cases([
            (0.000000013, 0.25),
            (0.123456789, 0.234567891),
            (123456.789, 0.0000123456789),
        ])

    def test_varied_arguments_and_repeated_calls(self):
        self.check_cases([(3, 1.5), (3, 4.75), (200, 0.03), (12, 1.5), (3, 1.5)])


if __name__ == "__main__":
    unittest.main()

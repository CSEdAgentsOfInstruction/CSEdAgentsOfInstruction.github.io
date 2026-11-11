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


class TestExpedition(BehaviorTest):
    FUNCTIONS = ("total_distance", "average_distance", "count_long_stages", "summarize_route")

    def check_calculation(self, name, values, expected, *args):
        original = list(values)
        result = self.calculation(name, values, *args)
        self.assertAlmostEqual(result, expected, places=7)
        self.assertEqual(values, original)

    def test_totals_include_every_stage(self):
        for values in [[], [5], [1.5, 2.5, 0], [4, 7, 3, 10], [3, 3, 3], [0, 0]]:
            with self.subTest(values=values): self.check_calculation("total_distance", values, sum(values))

    def test_averages_of_nonempty_lists(self):
        for values in [[5], [2, 3], [0, 0], [0.5, 1, 2], [4, 7, 3, 10]]:
            with self.subTest(values=values): self.check_calculation("average_distance", values, sum(values) / len(values))

    def test_counts_use_the_boundary_parameter(self):
        for values, minimum in [([], 7), ([7], 7), ([6, 7, 8], 7), ([0, 2, 4], 5), ([0, 0, 2], 0), ([1.5, 1.5, 2], 1.5)]:
            with self.subTest(values=values, minimum=minimum):
                self.check_calculation("count_long_stages", values, sum(value >= minimum for value in values), minimum)

    def test_summary_order_and_unchanged_inputs(self):
        for values, minimum in [([4, 7, 3, 10], 7), ([2.5], 2.5), ([0, 1, 2], 5), ([7, 7, 7], 7)]:
            original = list(values)
            result = self.calculation("summarize_route", values, minimum)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)
            self.assertAlmostEqual(result[0], sum(values))
            self.assertAlmostEqual(result[1], sum(values) / len(values))
            self.assertEqual(result[2], sum(value >= minimum for value in values))
            self.assertEqual(values, original)

    def test_average_uses_the_returned_total(self):
        with patch.object(self.module, "total_distance", autospec=True, return_value=15) as total:
            self.assertEqual(self.calculation("average_distance", [1, 2, 3]), 5)
            total.assert_any_call([1, 2, 3])

    def test_summary_uses_all_returned_results(self):
        values = [2, 4]
        with patch.object(self.module, "total_distance", autospec=True, return_value=21) as total, patch.object(self.module, "average_distance", autospec=True, return_value=8) as average, patch.object(self.module, "count_long_stages", autospec=True, return_value=0) as count:
            self.assertEqual(self.calculation("summarize_route", values, 3), [21, 8, 0])
            total.assert_any_call(values)
            average.assert_any_call(values)
            count.assert_any_call(values, 3)


if __name__ == "__main__":
    unittest.main()

# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import time_limit
import contextlib
import importlib.util
import io
import os
import unittest
from unittest.mock import patch


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")





class TestRecordAnotherReading(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("student_solution", SCRIPT_PATH)
        self.module = importlib.util.module_from_spec(spec)
        output = io.StringIO()
        with time_limit(), patch("builtins.input", side_effect=AssertionError("Do not read input.")), contextlib.redirect_stdout(output):
            spec.loader.exec_module(self.module)
        self.assertEqual(output.getvalue(), "", "Remove temporary top-level output before submitting.")
        self.assertTrue(callable(getattr(self.module, "with_reading_added", None)), "Define with_reading_added(readings, reading).")

    def call(self, readings, reading):
        original = list(readings)
        output = io.StringIO()
        with time_limit(), patch("builtins.input", side_effect=AssertionError("Do not read input.")), contextlib.redirect_stdout(output):
            result = self.module.with_reading_added(readings, reading)
        self.assertEqual(output.getvalue(), "", "Return the new log without printing it.")
        self.assertIsInstance(result, list, "Return a list containing the original readings and the new reading.")
        self.assertEqual(result, original + [reading], "Preserve the original order and repeated values, then add the new reading at the end.")
        self.assertEqual(readings, original, "Leave the supplied log unchanged.")
        self.assertIsNot(result, readings, "The returned log must be a separate list.")
        return result

    def test_empty_single_and_zero_readings(self):
        for readings, reading in [([], 0), ([], -2.5), ([7], 7), ([0], 0), ([-4], 1.25)]:
            with self.subTest(readings=readings, reading=reading):
                self.call(readings, reading)

    def test_order_repetition_and_decimal_values(self):
        cases = [
            ([4, -2, 0, 4], 1.5),
            ([-0.25, 0, 1.75, -0.25], -3.5),
            ([8, 3, 8, 1, 8], 3),
            ([50, -8, 12, 0, 3, 50, -2], -2),
        ]
        for readings, reading in cases:
            with self.subTest(readings=readings, reading=reading):
                self.call(readings, reading)

    def test_changes_to_either_log_stay_separate(self):
        for original in [[], [4, 0, -2, 4]]:
            with self.subTest(original=original):
                readings = list(original)
                result = self.call(readings, 2.5)
                result[0] = 999
                result.append(-999)
                self.assertEqual(readings, original, "Changing the returned list must not change the original log.")
                returned_values = list(result)
                readings.append(123)
                readings[0] = -123
                self.assertEqual(result, returned_values, "Changing the original log must not change a previously returned list.")

    def test_each_call_has_an_independent_result(self):
        readings = [5, -1, 5]
        first = self.call(readings, 0)
        second = self.call(readings, 2.5)
        empty_result = self.call([], -3)
        self.assertEqual(first, [5, -1, 5, 0], "Later calls must not change an earlier result.")
        self.assertEqual(second, [5, -1, 5, 2.5], "Each call must use that call's readings and additional reading.")
        self.assertIsNot(first, second, "Each call must return a separate list.")
        first.append(99)
        self.assertEqual(second, [5, -1, 5, 2.5], "Results from different calls must stay independent.")
        self.assertEqual(empty_result, [-3])
        self.assertEqual(readings, [5, -1, 5])


if __name__ == "__main__":
    unittest.main()

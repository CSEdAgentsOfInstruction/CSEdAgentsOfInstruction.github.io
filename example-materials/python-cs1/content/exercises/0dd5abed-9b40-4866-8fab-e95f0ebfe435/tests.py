# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import math
import os
import sys
import unittest
from decimal import Decimal, InvalidOperation


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestRainfallAnalysis(unittest.TestCase):
    def assert_numeric_result(self, actual, expected, mistake_hint):
        # Allow ordinary floating-point arithmetic differences, while retaining
        # the significant digits in small measurements and repeating averages.
        self.assertTrue(
            math.isfinite(actual)
            and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=0.0),
            mistake_hint + f"\nExpected {expected!r}, but the program printed {actual!r}.",
        )

    def run_program(self, entered_lines, mistake_hint):
        try:
            result = run_script(SCRIPT_PATH, input='\n'.join(entered_lines) + '\n')
        except TimeoutError:
            self.fail(
                "The program did not stop within three seconds. Convert the input "
                "to a number, compare it with 9999, and run break before storing "
                "the sentinel. "
                + mistake_hint
            )

        self.assertEqual(
            result.returncode,
            0,
            "The program must run successfully. "
            + mistake_hint
            + f"\nPython reported:\n{result.stderr}",
        )
        return result.stdout.splitlines()

    def assert_summary(
        self,
        entered_lines,
        expected_entered,
        expected_valid,
        expected_total,
        expected_average,
        mistake_hint,
    ):
        actual_lines = self.run_program(entered_lines, mistake_hint)
        prefixes = [
            "Measurements entered: ",
            "Valid readings: ",
            "Total rainfall: ",
            "Average rainfall: ",
        ]

        self.assertEqual(
            len(actual_lines),
            4,
            "Print exactly four summary lines and do not display input prompts. "
            + mistake_hint
            + f"\nThe program printed: {actual_lines!r}",
        )

        values = []
        for line, prefix in zip(actual_lines, prefixes):
            self.assertTrue(
                line.startswith(prefix),
                f"Line {len(values) + 1} must begin with {prefix!r}. "
                + mistake_hint
                + f"\nThe line was: {line!r}",
            )
            values.append(line[len(prefix) :].strip())

        try:
            counts = [Decimal(value) for value in values[:2]]
            if any(
                not count.is_finite() or count != count.to_integral_value()
                for count in counts
            ):
                raise ValueError("Counts must be finite whole numbers.")
            actual_entered, actual_valid = [int(count) for count in counts]
            actual_total = float(values[2])
        except (ValueError, InvalidOperation):
            self.fail(
                "The first two results must be whole-number counts and Total "
                "rainfall must be numeric. "
                + mistake_hint
                + f"\nThe printed values were: {values!r}"
            )

        self.assertEqual(
            actual_entered,
            expected_entered,
            "Measurements entered must count every non-sentinel input, including "
            "negative measurements that the filtering phase later discards. "
            + mistake_hint,
        )
        self.assertEqual(
            actual_valid,
            expected_valid,
            "Valid readings must count only the non-negative measurements. "
            + mistake_hint,
        )
        self.assert_numeric_result(
            actual_total,
            expected_total,
            "Total rainfall must add every valid reading once and must not "
            "include negative values or the sentinel. "
            + mistake_hint,
        )

        if expected_average is None:
            self.assertEqual(
                values[3],
                "none",
                "Print Average rainfall: none when there are no valid measurements. "
                + mistake_hint,
            )
        else:
            try:
                actual_average = float(values[3])
            except ValueError:
                self.fail(
                    "Average rainfall must be numeric when at least one valid "
                    "reading exists. "
                    + mistake_hint
                    + f"\nThe printed value was: {values[3]!r}"
                )
            self.assert_numeric_result(
                actual_average,
                expected_average,
                "Divide total rainfall by the number of valid readings, not "
                "by the number of all entered measurements. "
                + mistake_hint,
            )

    def test_immediate_sentinel(self):
        self.assert_summary(
            ["9999"],
            0,
            0,
            0,
            None,
            "The sentinel must stop collection before it is appended, and an "
            "empty valid list must not be used as a divisor.",
        )

    def test_only_negative_measurements(self):
        self.assert_summary(
            ["-2", "-4.5", "9999"],
            2,
            0,
            0,
            None,
            "Keep negative non-sentinel inputs among the original measurements, "
            "but exclude them from the valid measurements. Check whether any "
            "valid measurements remain.",
        )

    def test_zero_is_valid(self):
        self.assert_summary(
            ["-3", "0", "9999"],
            2,
            1,
            0,
            0,
            "Zero is a valid measurement and must be kept when filtering.",
        )

    def test_mixed_decimal_measurements(self):
        self.assert_summary(
            ["1.5", "-0.25", "2.5", "0", "6", "9999"],
            5,
            4,
            10,
            2.5,
            "Every negative value, including a negative fraction close to zero, "
            "must be filtered out. Use the number of valid measurements for the average.",
        )

    def test_average_uses_normal_division_without_rounding(self):
        self.assert_summary(
            ["2", "3", "5", "9999"],
            3,
            3,
            10,
            10 / 3,
            "Use / rather than // and print Python's ordinary division result "
            "without rounding it.",
        )

    def test_numeric_sentinel_form_stops_at_once(self):
        self.assert_summary(
            ["1.25", "9999.0", "100", "9999"],
            1,
            1,
            1.25,
            1.25,
            "Convert input with float before comparing it with numeric 9999. "
            "The values after the first sentinel must not be read.",
        )

    def test_preserves_small_measurements_and_fractional_results(self):
        for measurements in [
            [0.000000013, 0, 0.000000021],
            [0.123456789, 0.234567891, -0.01, 0],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        ]:
            with self.subTest(measurements=measurements):
                valid = [reading for reading in measurements if reading >= 0]
                total = sum(valid)
                self.assert_summary(
                    [str(reading) for reading in measurements] + ["9999"],
                    len(measurements),
                    len(valid),
                    total,
                    total / len(valid),
                    "Keep the numeric measurements and print the ordinary "
                    "arithmetic results without rounding them.",
                )

    def test_normalizes_numeric_sentinel_forms(self):
        for sentinel in [" 9999 ", "9.999e3", "+9999.00"]:
            with self.subTest(sentinel=sentinel):
                self.assert_summary([sentinel, "12"], 0, 0, 0, None,
                                    "All numeric spellings of the sentinel end input immediately.")

    def test_repeated_and_longer_measurement_series(self):
        measurements = [0, 2.5, -1, 2.5] * 10
        self.assert_summary([str(v) for v in measurements] + ["9999"],
                            40, 30, 50, 50 / 30,
                            "Keep repeated readings and include every valid zero in the average's count.")

    def test_single_measurements(self):
        for reading in ["0", "-0.0", "0.125", "15000", "-12"]:
            with self.subTest(reading=reading):
                value = float(reading)
                valid = value >= 0
                self.assert_summary([reading, "9999"], 1, int(valid),
                                    value if valid else 0, value if valid else None,
                                    "Only 9999 ends input; other non-negative numbers are valid data.")


if __name__ == "__main__":
    unittest.main()

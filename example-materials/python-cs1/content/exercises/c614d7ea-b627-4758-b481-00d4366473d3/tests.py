# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestAverageSpeed(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_accepts_decimal_inputs_and_calculates_speed(self):
        cases = [
            (1.25, 0.5, "2.5 km/h"),
            (7.5, 2.5, "3.0 km/h"),
        ]
        for distance, time, expected in cases:
            with self.subTest(distance=distance, time=time):
                result = run_script(self.script_path(), input=f'{distance}\n{time}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    "Read both decimal inputs and calculate their average speed. "
                    f"Python reported:\n{result.stderr}",
                )
                self.assertEqual(result.stdout.strip(), expected)

    def test_formats_the_speed_with_one_decimal_place(self):
        cases = [
            (150, 2, "75.0 km/h"),
            (100, 3, "33.3 km/h"),
            (1.5, 0.5, "3.0 km/h"),
        ]
        for distance, time, expected in cases:
            with self.subTest(distance=distance, time=time):
                result = run_script(self.script_path(), input=f'{distance}\n{time}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip(),
                    expected,
                    "Calculate average speed as distance divided by time, then print "
                    "the result with exactly one decimal place followed by km/h.",
                )


if __name__ == "__main__":
    unittest.main()

# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestBatteryClassifier(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_boundary_values(self):
        cases = [
            (0, "Low battery"),
            (19, "Low battery"),
            (20, "Battery okay"),
            (79, "Battery okay"),
            (80, "Battery high"),
            (100, "Battery high"),
        ]
        for percentage, expected in cases:
            with self.subTest(percentage=percentage):
                result = run_script(self.script_path(), input=f'{percentage}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip(),
                    expected,
                    f"A battery percentage of {percentage} must print exactly "
                    f"{expected!r}. Check the boundaries at 20 and 80.",
                )


if __name__ == "__main__":
    unittest.main()

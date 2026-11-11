# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestFreezingCheck(unittest.TestCase):
    def test_negative_temperatures_are_below_freezing(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")

        for entered, expected in [
            (-5, "Below freezing"),
            (-1, "Below freezing"),
            ("-0", "Not below freezing"),
            (0, "Not below freezing"),
            ("+5", "Not below freezing"),
            (12, "Not below freezing"),
        ]:
            with self.subTest(entered=entered):
                try:
                    result = run_script(script_path, input=f'{entered}\n')
                except TimeoutError:
                    self.fail("The program did not finish after reading one temperature.")
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.splitlines(),
                    [expected],
                    "Convert the input to a number, compare it with zero, and print only the applicable message.",
                )


if __name__ == "__main__":
    unittest.main()

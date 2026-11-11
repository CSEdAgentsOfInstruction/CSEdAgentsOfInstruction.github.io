# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestConfirmationCheck(unittest.TestCase):
    def test_confirmation_ignores_case_and_surrounding_whitespace(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")

        for entered, expected in [
            ("yes", "Confirmed"),
            ("YES", "Confirmed"),
            (" Yes ", "Confirmed"),
            ("\tYeS\t", "Confirmed"),
            ("no", "Not confirmed"),
            ("maybe", "Not confirmed"),
            ("yesterday", "Not confirmed"),
            ("y", "Not confirmed"),
        ]:
            with self.subTest(entered=entered):
                try:
                    result = run_script(script_path, input=f'{entered}\n')
                except TimeoutError:
                    self.fail("The program did not finish after reading one confirmation.")
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.splitlines(),
                    [expected],
                    "Remove surrounding whitespace, ignore letter case, and print only the applicable message.",
                )


if __name__ == "__main__":
    unittest.main()

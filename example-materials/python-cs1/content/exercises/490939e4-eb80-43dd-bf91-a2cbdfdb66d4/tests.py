# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestSeniorDiscountBoundary(unittest.TestCase):
    def test_discount_includes_age_65(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")

        for entered, expected in [
            (64, "Standard price"),
            (65, "Senior discount"),
            (66, "Senior discount"),
        ]:
            with self.subTest(entered=entered):
                try:
                    result = run_script(script_path, input=f'{entered}\n')
                except TimeoutError:
                    self.fail("The program did not finish after reading one age.")
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.splitlines(),
                    [expected],
                    "Include age 65 in the senior-discount group and print only the applicable message.",
                )


if __name__ == "__main__":
    unittest.main()

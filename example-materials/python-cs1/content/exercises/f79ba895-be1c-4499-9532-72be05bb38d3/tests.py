# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestAccessCondition(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_all_truth_combinations_and_age_boundary(self):
        cases = [
            (15, "yes", "False"),
            (16, "yes", "True"),
            (21, " YES ", "True"),
            (16, "no", "False"),
            (15, "no", "False"),
        ]
        for age, agreement, expected in cases:
            with self.subTest(age=age, agreement=agreement):
                result = run_script(self.script_path(), input=f'{age}\n{agreement}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip(),
                    expected,
                    "The result is true only when the user is at least 16 and the "
                    "normalized agreement answer is 'yes'.",
                )


if __name__ == "__main__":
    unittest.main()

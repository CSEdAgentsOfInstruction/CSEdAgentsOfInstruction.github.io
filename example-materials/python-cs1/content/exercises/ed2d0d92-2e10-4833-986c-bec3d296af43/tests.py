# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestResultReport(unittest.TestCase):
    def test_result_is_always_recorded(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")

        for entered, expected in [
            (69, "Not yet\nResult recorded."),
            (70, "Pass\nResult recorded."),
            (95, "Pass\nResult recorded."),
        ]:
            with self.subTest(entered=entered):
                try:
                    result = run_script(script_path, input=f'{entered}\n')
                except TimeoutError:
                    self.fail("The program did not finish after reading one score.")
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.splitlines(),
                    expected.splitlines(),
                    "Print the result first and 'Result recorded.' second for every score, with no extra output.",
                )


if __name__ == "__main__":
    unittest.main()

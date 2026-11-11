# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestAccessCheck(unittest.TestCase):
    def test_access_depends_on_exact_input(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")

        for entered, expected in [
            ("green", "Access granted"),
            ("blue", "Access denied"),
            ("Green", "Access denied"),
            (" green ", "Access denied"),
            ("g", "Access denied"),
        ]:
            with self.subTest(entered=entered):
                try:
                    result = run_script(script_path, input=f'{entered}\n')
                except TimeoutError:
                    self.fail("The program did not finish after reading one access code.")
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.splitlines(),
                    [expected],
                    "Print only the message for the exact code entered. Do not normalize the code or print extra output.",
                )


if __name__ == "__main__":
    unittest.main()

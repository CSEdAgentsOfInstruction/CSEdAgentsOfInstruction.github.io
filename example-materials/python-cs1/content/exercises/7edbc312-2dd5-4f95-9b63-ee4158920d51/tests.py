# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestProgram(unittest.TestCase):
    def test_output(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        try:
            result = run_script(script_path)
        except TimeoutError:
            self.fail("The program did not finish. Check that it only prints the requested line.")

        self.assertEqual(
            result.returncode,
            0,
            f"The program must run without a syntax error. Python reported:\n{result.stderr}",
        )
        self.assertEqual(
            result.stdout.splitlines(),
            ["Welcome!"],
            "Print exactly one line containing 'Welcome!' with no extra output.",
        )


if __name__ == "__main__":
    unittest.main()

# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestWelcomeCard(unittest.TestCase):
    def test_prints_welcome_card_exactly(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        result = run_script(script_path)

        self.assertEqual(
            result.returncode,
            0,
            f"The program must run successfully. Python reported:\n{result.stderr}",
        )

        self.assertEqual(
            result.stdout,
            "********\nWelcome!\n********\n",
            "The output must match the welcome card exactly.",
        )


if __name__ == "__main__":
    unittest.main()

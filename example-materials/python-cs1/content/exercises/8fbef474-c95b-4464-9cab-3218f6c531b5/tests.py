# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestPersonalizedOutput(unittest.TestCase):
    def test_prints_the_required_sentence(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        for name, hometown in [("Ada", "London"), ("Grace", "Helsinki")]:
            with self.subTest(name=name, hometown=hometown):
                result = run_script(script_path, input=f'{name}\n{hometown}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertTrue(
                    result.stdout.endswith(f"{name} is from {hometown}.\n"),
                    "Print the final sentence in the form "
                    f"'{name} is from {hometown}.', using the entered values in "
                    "their correct roles.",
                )


if __name__ == "__main__":
    unittest.main()

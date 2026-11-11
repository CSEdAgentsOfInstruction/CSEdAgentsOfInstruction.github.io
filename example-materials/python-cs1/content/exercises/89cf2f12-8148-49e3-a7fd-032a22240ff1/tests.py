# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestNameAndAge(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_asks_for_name_before_integer_age(self):
        result = run_script(self.script_path(), input='Ada\n037\n')
        self.assertEqual(
            result.returncode,
            0,
            "Read the name first, then read and convert the whole-number age. "
            f"Python reported:\n{result.stderr}",
        )
        self.assertTrue(
            result.stdout.endswith("Hello Ada! You are 37 years old.\n"),
            "Read the name before the age and use the integer age in the greeting.",
        )

    def test_prints_the_required_greeting(self):
        cases = [("Ada", 37), ("Lin", 8), ("Grace Hopper", 85)]
        for name, age in cases:
            with self.subTest(name=name, age=age):
                result = run_script(self.script_path(), input=f'{name}\n{age}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertTrue(
                    result.stdout.endswith(
                        f"Hello {name}! You are {age} years old.\n"
                    ),
                    "Print the greeting exactly as shown in the exercise.",
                )

if __name__ == "__main__":
    unittest.main()

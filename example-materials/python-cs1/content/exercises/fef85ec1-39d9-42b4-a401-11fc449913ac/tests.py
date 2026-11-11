# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestRepeatedResponse(unittest.TestCase):
    def test_prints_the_entered_food_twice(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        for food in ["Noodles", "Berry tart"]:
            with self.subTest(food=food):
                try:
                    result = run_script(script_path, input=f'{food}\n')
                except TimeoutError:
                    self.fail("The program did not finish after one food was entered.")

                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertTrue(
                    result.stdout.startswith("Favorite food? "),
                    "Keep the existing favorite-food prompt.",
                )
                responses = result.stdout.removeprefix("Favorite food? ").splitlines()
                self.assertEqual(
                    responses,
                    [food, food],
                    "Print the current food twice, each on its own line.",
                )


if __name__ == "__main__":
    unittest.main()

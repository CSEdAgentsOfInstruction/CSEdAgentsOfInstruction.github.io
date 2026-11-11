# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestChangedProfile(unittest.TestCase):
    def test_required_prompts_and_values_are_present(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        profiles = [
            ("Ada", "Helsinki", "tea", "Python"),
            ("Grace", "Turku", "pasta", "JavaScript"),
        ]
        for profile in profiles:
            with self.subTest(profile=profile):
                _name, _hometown, food, language = profile
                result = run_script(script_path, input='\n'.join(profile) + '\n')

                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertIn(
                    "Hometown: ", result.stdout, "Change the City prompt to Hometown."
                )
                self.assertNotIn(
                    "City: ", result.stdout, "The old City prompt should be replaced."
                )
                self.assertIn(
                    "Favorite food: ",
                    result.stdout,
                    "Keep the existing favorite-food prompt.",
                )
                self.assertIn(
                    "Favorite programming language: ",
                    result.stdout,
                    "Add the required favorite-programming-language prompt.",
                )
                self.assertLess(
                    result.stdout.index("Favorite food: "),
                    result.stdout.index("Favorite programming language: "),
                    "Ask for the favorite programming language after the favorite food.",
                )
                final_output = result.stdout.rsplit(
                    "Favorite programming language: ", maxsplit=1
                )[-1]
                for line in final_output.splitlines():
                    normalized_line = line.casefold()
                    contains_role_value = food in line or language in line
                    if "favorite food" in normalized_line and contains_role_value:
                        self.assertIn(
                            food,
                            line,
                            "Do not swap the favorite food and programming language in labeled output.",
                        )
                    if "programming language" in normalized_line and contains_role_value:
                        self.assertIn(
                            language,
                            line,
                            "Do not swap the favorite food and programming language in labeled output.",
                        )
                for value in profile:
                    self.assertIn(
                        value,
                        result.stdout,
                        f"The final output should include the entered value {value!r}.",
                    )


if __name__ == "__main__":
    unittest.main()

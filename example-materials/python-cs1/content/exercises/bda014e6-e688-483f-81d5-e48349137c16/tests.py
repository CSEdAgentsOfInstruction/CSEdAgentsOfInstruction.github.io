# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestNormalizeAnswer(unittest.TestCase):
    def test_uses_strip_and_lower(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        with open(script_path, encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        called_methods = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertIn("strip", called_methods, "Use .strip() to remove surrounding whitespace.")
        self.assertIn("lower", called_methods, "Use .lower() to produce lowercase text.")

    def test_inputs_are_cleaned_and_lowercased(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        cases = [
            ("yes", "yes"),
            ("YES", "yes"),
            (" Yes ", "yes"),
            ("no", "no"),
            ("NO", "no"),
            (" No ", "no"),
        ]
        for user_input, expected in cases:
            with self.subTest(user_input=user_input):
                result = run_script(script_path, input=f'{user_input}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertTrue(
                    result.stdout.rstrip().endswith(expected),
                    f"The input {user_input!r} should be stored and printed as "
                    f"{expected!r}.",
                )


if __name__ == "__main__":
    unittest.main()

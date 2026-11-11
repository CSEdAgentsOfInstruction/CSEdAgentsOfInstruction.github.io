# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestGreetingRepair(unittest.TestCase):
    def test_uses_an_f_string(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        with open(script_path, encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        self.assertTrue(
            any(isinstance(node, ast.JoinedStr) for node in ast.walk(tree)),
            "Add the missing f before the greeting string.",
        )

    def test_greeting_uses_the_entered_name(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        for name in ["Ada", "Grace"]:
            with self.subTest(name=name):
                result = run_script(script_path, input=f'{name}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertTrue(
                    result.stdout.rstrip().endswith(f"Hello, {name}!"),
                    "Insert the entered name into the greeting exactly as shown. "
                    "Check both the f-string marker and the lowercase name variable.",
                )


if __name__ == "__main__":
    unittest.main()

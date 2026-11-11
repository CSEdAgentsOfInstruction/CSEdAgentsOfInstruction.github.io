# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestFixedNumericInput(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_converts_input_to_an_integer(self):
        with open(self.script_path(), encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        self.assertTrue(
            any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "int"
                for node in ast.walk(tree)
            ),
            "Convert the entered text with int(...).",
        )

    def test_adds_five_numerically(self):
        for entered, expected in [(12, "17"), (0, "5"), (-8, "-3"), (100, "105")]:
            with self.subTest(entered=entered):
                try:
                    result = run_script(self.script_path(), input=f'{entered}\n')
                except TimeoutError:
                    self.fail("The program did not finish after reading one number.")
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.splitlines(),
                    [expected],
                    "Add 5 to the numeric input and print only the calculated number.",
                )


if __name__ == "__main__":
    unittest.main()

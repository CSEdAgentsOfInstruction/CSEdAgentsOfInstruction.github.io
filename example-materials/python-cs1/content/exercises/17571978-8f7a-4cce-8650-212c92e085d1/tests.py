# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestPizzasToOrder(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_uses_integer_arithmetic(self):
        with open(self.script_path(), encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        int_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "int"
        ]
        self.assertGreaterEqual(
            len(int_calls),
            2,
            "Convert both entered values with int(...).",
        )
        operators = {
            type(node.op)
            for node in ast.walk(tree)
            if isinstance(node, ast.BinOp)
        }
        self.assertIn(ast.Mult, operators, "Multiply people by slices per person.")
        self.assertIn(
            ast.FloorDiv,
            operators,
            "Use floor division to calculate a whole number of pizzas.",
        )

    def test_rounds_partial_pizzas_up(self):
        cases = [
            (4, 2, "Pizzas: 1"),
            (5, 2, "Pizzas: 2"),
            (1, 9, "Pizzas: 2"),
            (8, 3, "Pizzas: 3"),
            (9, 3, "Pizzas: 4"),
        ]
        for people, slices_per_person, expected in cases:
            with self.subTest(people=people, slices_per_person=slices_per_person):
                result = run_script(self.script_path(), input=f'{people}\n{slices_per_person}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip(),
                    expected,
                    "Print the number of whole pizzas needed, rounding partial pizzas up.",
                )


if __name__ == "__main__":
    unittest.main()

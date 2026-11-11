# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestTimeConversion(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_uses_floor_division_and_remainder(self):
        with open(self.script_path(), encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        operators = {
            type(node.op)
            for node in ast.walk(tree)
            if isinstance(node, ast.BinOp)
        }
        self.assertIn(
            ast.FloorDiv,
            operators,
            "Calculate complete hours with floor division: total_minutes // 60.",
        )
        self.assertIn(
            ast.Mod,
            operators,
            "Calculate leftover minutes with the remainder operator: total_minutes % 60.",
        )

        assigned_names = {
            target.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        self.assertTrue(
            {"total_minutes", "hours", "minutes"}.issubset(assigned_names),
            "Use the variables total_minutes, hours, and minutes.",
        )

    def test_prints_hours_before_leftover_minutes(self):
        cases = [
            (135, ["Hours: 2", "Minutes: 15"]),
            (59, ["Hours: 0", "Minutes: 59"]),
            (120, ["Hours: 2", "Minutes: 0"]),
            (1501, ["Hours: 25", "Minutes: 1"]),
        ]
        for total_minutes, expected_lines in cases:
            with self.subTest(total_minutes=total_minutes):
                result = run_script(self.script_path(), input=f'{total_minutes}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip().splitlines(),
                    expected_lines,
                    "Print exactly the Hours line followed by the Minutes line.",
                )


if __name__ == "__main__":
    unittest.main()

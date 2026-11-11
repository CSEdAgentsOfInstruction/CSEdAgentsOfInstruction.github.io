# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestConditionalMessage(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_has_an_if_and_a_later_top_level_statement(self):
        with open(self.script_path(), encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        if_positions = [
            index for index, node in enumerate(tree.body) if isinstance(node, ast.If)
        ]
        self.assertTrue(if_positions, "Use an if statement for the freezing warning.")
        self.assertTrue(
            any(
                index > if_positions[0]
                and isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Call)
                for index, node in enumerate(tree.body)
            ),
            "Keep the final print outside and after the if statement.",
        )

    def test_warning_is_conditional_and_final_line_always_runs(self):
        cases = [
            (-10, ["Warning: below freezing.", "Temperature checked."]),
            (-1, ["Warning: below freezing.", "Temperature checked."]),
            (0, ["Temperature checked."]),
            (18, ["Temperature checked."]),
        ]
        for temperature, expected_lines in cases:
            with self.subTest(temperature=temperature):
                result = run_script(self.script_path(), input=f'{temperature}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip().splitlines(),
                    expected_lines,
                    "Print the warning only for temperatures below zero, and always "
                    "print 'Temperature checked.' after the decision.",
                )


if __name__ == "__main__":
    unittest.main()

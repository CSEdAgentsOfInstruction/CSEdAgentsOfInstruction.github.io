# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestDepartureAdviceBranchOrder(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_uses_one_if_elif_else_chain(self):
        with open(self.script_path(), encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        top_level_ifs = [node for node in tree.body if isinstance(node, ast.If)]
        self.assertEqual(
            len(top_level_ifs),
            1,
            "Use one if/elif/else chain rather than separate if statements.",
        )
        first_if = top_level_ifs[0]
        self.assertTrue(
            first_if.orelse and isinstance(first_if.orelse[0], ast.If),
            "Use elif for the second departure category.",
        )
        elif_node = first_if.orelse[0]
        self.assertTrue(
            elif_node.orelse,
            "Use else for the final departure category.",
        )

    def test_all_departure_categories(self):
        cases = [
            (0, "Leave now."),
            (9, "Leave now."),
            (10, "Get ready."),
            (29, "Get ready."),
            (30, "Plenty of time."),
            (60, "Plenty of time."),
        ]
        for minutes, expected in cases:
            with self.subTest(minutes=minutes):
                result = run_script(self.script_path(), input=f'{minutes}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip(),
                    expected,
                    f"With {minutes} minutes until departure, print exactly "
                    f"{expected!r}. Check the branch order and the boundaries at "
                    "10 and 30 minutes.",
                )


if __name__ == "__main__":
    unittest.main()

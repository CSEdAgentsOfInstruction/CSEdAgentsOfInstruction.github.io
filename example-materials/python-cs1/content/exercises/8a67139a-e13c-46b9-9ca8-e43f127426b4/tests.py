# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestProgram(unittest.TestCase):
    def test_replaces_items_with_an_indexed_loop(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                tree = ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"The program must contain valid Python. Python reported: {error}")

        def loop_target_names(target):
            return {
                node.id
                for node in ast.walk(target)
                if isinstance(node, ast.Name)
            }

        def is_indexed_energy_target(target, index_names):
            return (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == "energy_levels"
                and isinstance(target.slice, ast.Name)
                and target.slice.id in index_names
            )

        found_indexed_replacement = False
        for loop in (node for node in ast.walk(tree) if isinstance(node, ast.For)):
            index_names = loop_target_names(loop.target)
            for node in ast.walk(loop):
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                elif isinstance(node, ast.AugAssign):
                    targets = [node.target]
                if any(
                    is_indexed_energy_target(target, index_names)
                    for target in targets
                ):
                    found_indexed_replacement = True

        self.assertTrue(
            found_indexed_replacement,
            "Use the loop's index to replace items in energy_levels itself, for example energy_levels[index] = 0.",
        )

    def assert_program(self, entered_lines, expected_lines):
        try:
            result = run_script(SCRIPT_PATH, input='\n'.join((str(value) for value in entered_lines)) + '\n')
        except TimeoutError:
            self.fail(
                "The program did not finish. Check the number of inputs "
                "and the loop's stopping condition."
            )
        self.assertEqual(
            result.returncode, 0,
            f"The program must run for these inputs. Python reported:\n{result.stderr}",
        )
        self.assertEqual(
            result.stdout.splitlines(), expected_lines,
            "Check the result for these inputs, including order, repeated values, "
            "and boundaries. Print only the requested output.",
        )

    def test_repairs_example_readings(self):
        cases = [
            ([4, 80, -15, 45, -4], ['[80, 0, 45, 0]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_single_lists(self):
        cases = [
            ([0], ['[]']),
            ([1, -1], ['[0]']),
            ([1, 0], ['[0]']),
            ([1, 5], ['[5]']),
            ([1, 101], ['[101]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_changes_only_negative_items(self):
        cases = [
            ([5, -1, 0, 2, -3, 4], ['[0, 0, 2, 0, 4]']),
            ([3, -2, -2, -2], ['[0, 0, 0]']),
            ([5, -1, 101, 1000, 0, 101], ['[0, 101, 1000, 0, 101]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_processes_every_position(self):
        cases = [
            (
                [
                    21, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7,
                    8, 9, 10,
                ],
                ['[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

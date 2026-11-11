# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestProgram(unittest.TestCase):
    def test_uses_a_data_candidate_and_best_so_far_loop(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                tree = ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"The program must contain valid Python. Python reported: {error}")

        def is_temperature_item(node):
            return (
                isinstance(node, ast.Subscript)
                and isinstance(node.value, ast.Name)
                and node.value.id == "temperatures"
                and not isinstance(node.slice, ast.Slice)
            )

        def initializes_lowest_from_data(node):
            if isinstance(node, ast.Assign):
                assigns_lowest = any(
                    isinstance(target, ast.Name) and target.id == "lowest"
                    for target in node.targets
                )
                value = node.value
            elif isinstance(node, ast.AnnAssign):
                assigns_lowest = (
                    isinstance(node.target, ast.Name) and node.target.id == "lowest"
                )
                value = node.value
            else:
                return False
            return assigns_lowest and is_temperature_item(value)

        self.assertTrue(
            any(initializes_lowest_from_data(node) for node in ast.walk(tree)),
            "Initialize lowest from an item in temperatures, such as temperatures[0].",
        )

        def loops_over_temperatures(node):
            return (
                isinstance(node, ast.For)
                and (
                    (
                        isinstance(node.iter, ast.Name)
                        and node.iter.id == "temperatures"
                    )
                    or (
                        isinstance(node.iter, ast.Subscript)
                        and isinstance(node.iter.value, ast.Name)
                        and node.iter.value.id == "temperatures"
                    )
                )
            )

        candidate_loops = [
            node for node in ast.walk(tree) if loops_over_temperatures(node)
        ]
        self.assertTrue(
            candidate_loops,
            "Use a direct for loop over the stored temperatures.",
        )

        def updates_lowest(node):
            if isinstance(node, ast.Assign):
                return any(
                    isinstance(target, ast.Name) and target.id == "lowest"
                    for target in node.targets
                )
            if isinstance(node, ast.AnnAssign):
                return isinstance(node.target, ast.Name) and node.target.id == "lowest"
            return (
                isinstance(node, ast.AugAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == "lowest"
            )

        self.assertTrue(
            any(
                updates_lowest(descendant)
                for loop in candidate_loops
                for condition in loop.body
                if isinstance(condition, ast.If)
                for descendant in ast.walk(condition)
            ),
            "Inside the loop, update lowest only when the current temperature is lower.",
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

    def test_handles_mixed_signs(self):
        cases = [
            ([4, -2, 7, -8], ['Lowest: -8']),
            ([0, -1, 0, 1], ['Lowest: -1']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_positive_and_negative_lists(self):
        cases = [
            ([9, 3, 12, 6], ['Lowest: 3']),
            ([-7, -3, -12, -5], ['Lowest: -12']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_finds_minimum_at_each_position(self):
        cases = [
            ([-5, 1, 2, 3], ['Lowest: -5']),
            ([1, -5, 2, 3], ['Lowest: -5']),
            ([1, 2, -5, 3], ['Lowest: -5']),
            ([1, 2, 3, -5], ['Lowest: -5']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_equal_values(self):
        cases = [
            ([2, 2, 2, 2], ['Lowest: 2']),
            ([-3, -3, -3, -3], ['Lowest: -3']),
            ([0, 0, 0, 0], ['Lowest: 0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_initial_candidate_comes_from_the_data(self):
        cases = [
            ([10000, 20000, 30000, 40000], ['Lowest: 10000']),
            ([5000000, 2000000, 7000000, 3000000], ['Lowest: 2000000']),
            ([10**12 + 3, 10**12 + 2, 10**12 + 1, 10**12],
             [f'Lowest: {10**12}']),
            ([-10**12, -10**12 - 1, 0, 1], [f'Lowest: {-10**12 - 1}']),
            ([2**53 + 7, 2**53 + 5, 2**53 + 3, 2**53 + 1],
             [f'Lowest: {2**53 + 1}']),
            ([-2**53 - 3, -2**53 - 1, 0, 1], [f'Lowest: {-2**53 - 3}']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

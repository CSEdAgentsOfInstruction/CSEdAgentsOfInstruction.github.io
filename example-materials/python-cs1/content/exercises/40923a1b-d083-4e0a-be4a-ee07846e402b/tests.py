# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestProgram(unittest.TestCase):
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

    def test_expands_example(self):
        cases = [
            ([3, 1, 2, 3], ['Original: [1, 2, 3]', 'Expanded: [1, 2, 2, 4, 3, 6]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_single_lists(self):
        cases = [
            ([0], ['Original: []', 'Expanded: []']),
            ([1, 0], ['Original: [0]', 'Expanded: [0, 0]']),
            ([1, -3], ['Original: [-3]', 'Expanded: [-3, -6]']),
            ([1, 2**53 + 1],
             [f'Original: [{2**53 + 1}]', f'Expanded: [{2**53 + 1}, {2**54 + 2}]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_input_order_and_duplicates(self):
        cases = [
            (
                [4, 2, -1, 2, 0],
                ['Original: [2, -1, 2, 0]', 'Expanded: [2, 4, -1, -2, 2, 4, 0, 0]'],
            ),
            (
                [4, 3, 3, 3, 3],
                ['Original: [3, 3, 3, 3]', 'Expanded: [3, 6, 3, 6, 3, 6, 3, 6]'],
            ),
            ([2, -2**53 - 1, -2**53 - 1],
             [f'Original: [{-2**53 - 1}, {-2**53 - 1}]',
              f'Expanded: [{-2**53 - 1}, {-2**54 - 2}, {-2**53 - 1}, {-2**54 - 2}]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_longer_lists(self):
        cases = [
            (
                [11, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
                [
                    'Original: [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]',
                    'Expanded: [-5, -10, -4, -8, -3, -6, -2, -4, -1, -2, 0, 0, 1, 2, 2, 4, 3, 6, 4, 8, 5, 10]',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

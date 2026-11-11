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

    def test_increments_example_scores(self):
        cases = [
            ([3, 5, 8, 10], ['[6, 9, 11]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_single_lists(self):
        cases = [
            ([0], ['[]']),
            ([1, 0], ['[1]']),
            ([1, -1], ['[0]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_increments_each_position_once(self):
        cases = [
            ([5, 2, -1, 8, 4, 0], ['[3, 0, 9, 5, 1]']),
            ([5, 5, 5, 5, 5, 5], ['[6, 6, 6, 6, 6]']),
            ([3, 2**53 + 1, -2**53 - 1, 0],
             [f'[{2**53 + 2}, {-2**53}, 1]']),
            ([2, 2**53 + 3, 2**53 + 3], [f'[{2**53 + 4}, {2**53 + 4}]']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_longer_lists(self):
        cases = [
            (
                [
                    21, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7,
                    8, 9, 10,
                ],
                [
                    '[-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

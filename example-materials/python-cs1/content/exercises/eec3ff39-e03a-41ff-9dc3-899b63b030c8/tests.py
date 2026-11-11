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

    def test_selects_example_values(self):
        cases = [
            ([5, 18, 21, 17, 23, 20], ['21', '23', '20']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_boundary_lists(self):
        cases = [
            ([0], []),
            ([1, 20], ['20']),
            ([1, 19], []),
            ([1, 21], ['21']),
            ([5, 19, 20, 21, -2, 20], ['20', '21', '20']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_no_matches_and_repetitions(self):
        cases = [
            ([3, -5, 0, 19], []),
            ([4, 100, 21, 100, 20], ['100', '21', '100', '20']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_longer_lists(self):
        cases = [
            (
                [
                    60, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8,
                    -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                    12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                ],
                [
                    '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                    '31', '32', '33', '34', '35', '36', '37', '38', '39',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

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

    def test_parses_mixed_temperatures_and_whitespace(self):
        cases = [
            (['-3 0 8 -1'], ['Temperatures: [-3, 0, 8, -1]', 'Below zero: 2']),
            (['  5   -2\t-7  0  '], ['Temperatures: [5, -2, -7, 0]', 'Below zero: 2']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_input(self):
        cases = [
            ([''], ['Temperatures: []', 'Below zero: 0']),
            (['   '], ['Temperatures: []', 'Below zero: 0']),
            (['\t'], ['Temperatures: []', 'Below zero: 0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_checks_zero_boundary(self):
        cases = [
            (['0'], ['Temperatures: [0]', 'Below zero: 0']),
            (['-1'], ['Temperatures: [-1]', 'Below zero: 1']),
            (['1'], ['Temperatures: [1]', 'Below zero: 0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_counts_repetitions_and_longer_lists(self):
        cases = [
            (['-2 -2 -2'], ['Temperatures: [-2, -2, -2]', 'Below zero: 3']),
            (['4 9 12'], ['Temperatures: [4, 9, 12]', 'Below zero: 0']),
            (
                [
                    '-20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20',
                ],
                [
                    'Temperatures: [-20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]',
                    'Below zero: 20',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_compares_numeric_values_for_different_integer_spellings(self):
        cases = [
            (['-0 +3 -1'], ['Temperatures: [0, 3, -1]', 'Below zero: 1']),
            (['+0 -00 000'], ['Temperatures: [0, 0, 0]', 'Below zero: 0']),
            (['+12 -002 003 -7'],
             ['Temperatures: [12, -2, 3, -7]', 'Below zero: 2']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

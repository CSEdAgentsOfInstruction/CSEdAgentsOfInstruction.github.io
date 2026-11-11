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

    def test_accepts_increasing_racks(self):
        cases = [
            ([1, 3, 5, 7, 9], ['Strictly increasing: True']),
            ([-9, -5, -2, 0, 4], ['Strictly increasing: True']),
            ([100, 200, 300, 400, 500], ['Strictly increasing: True']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_rejects_equal_neighbors(self):
        cases = [
            ([1, 3, 3, 7, 9], ['Strictly increasing: False']),
            ([1, 2, 3, 4, 4], ['Strictly increasing: False']),
            ([0, 0, 0, 0, 0], ['Strictly increasing: False']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_finds_decreases_at_different_positions(self):
        cases = [
            ([1, 5, 4, 7, 9], ['Strictly increasing: False']),
            ([1, 3, 5, 9, 8], ['Strictly increasing: False']),
            ([9, 1, 2, 3, 4], ['Strictly increasing: False']),
            ([9, 7, 5, 3, 1], ['Strictly increasing: False']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_rejects_an_isolated_equality_at_each_position(self):
        for position in range(4):
            cards = [-20, -10, 0, 10, 20]
            cards[position + 1] = cards[position]
            with self.subTest(equal_pair=position, cards=cards):
                self.assert_program(cards, ['Strictly increasing: False'])

    def test_rejects_an_isolated_decrease_at_each_position(self):
        for position in range(4):
            cards = [-20, -10, 0, 10, 20]
            cards[position + 1] = cards[position] - 1
            with self.subTest(decreasing_pair=position, cards=cards):
                self.assert_program(cards, ['Strictly increasing: False'])


if __name__ == "__main__":
    unittest.main()

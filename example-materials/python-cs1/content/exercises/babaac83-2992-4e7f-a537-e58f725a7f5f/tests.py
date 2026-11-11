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

    def test_compares_corresponding_positions(self):
        cases = [
            (['red blue green', 'red blue green'], ['Correct positions: 3 of 3']),
            (['red blue green', 'green blue red'], ['Correct positions: 1 of 3']),
            (
                ['one two three four', 'one too three five'],
                ['Correct positions: 2 of 4'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_repeated_and_single_words(self):
        cases = [
            (['go go stop', 'go stop stop'], ['Correct positions: 2 of 3']),
            (['cat', 'dog'], ['Correct positions: 0 of 1']),
            (['A', 'a'], ['Correct positions: 1 of 1']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_lines(self):
        cases = [
            (['', ''], ['Correct positions: 0 of 0']),
            ([' \t ', '   '], ['Correct positions: 0 of 0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_ignores_case_and_extra_whitespace(self):
        cases = [
            (['  RED blue  ', 'red BLUE'], ['Correct positions: 2 of 2']),
            (
                ['one   TWO\tthree', '  ONE two   THREE  '],
                ['Correct positions: 3 of 3'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_checks_the_final_position(self):
        cases = [
            (
                [
                    'go go go go go go go go go go go go go go go go go go go go',
                    'go go go go go go go go go go go go go go go go go go go stop',
                ],
                ['Correct positions: 19 of 20'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

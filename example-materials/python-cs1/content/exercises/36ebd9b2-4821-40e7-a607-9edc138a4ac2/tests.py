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

    def test_filters_example_words(self):
        cases = [
            (
                [4, 'sun', 'planet', 'sky', 'comet'],
                [
                    "Original: ['sun', 'planet', 'sky', 'comet']",
                    "Long words: ['planet', 'comet']",
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_single_lists(self):
        cases = [
            ([0], ['Original: []', 'Long words: []']),
            ([1, ''], ["Original: ['']", 'Long words: []']),
            ([1, 'five'], ["Original: ['five']", 'Long words: []']),
            ([1, 'comet'], ["Original: ['comet']", "Long words: ['comet']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_includes_exactly_five_characters(self):
        cases = [
            (
                [3, 'four', 'fives', 'longer'],
                [
                    "Original: ['four', 'fives', 'longer']",
                    "Long words: ['fives', 'longer']",
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_case_order_and_duplicates(self):
        cases = [
            (
                [4, 'PLANET', 'sun', 'comet', 'PLANET'],
                [
                    "Original: ['PLANET', 'sun', 'comet', 'PLANET']",
                    "Long words: ['PLANET', 'comet', 'PLANET']",
                ],
            ),
            (
                [
                    10, 'longword', 'longword', 'longword', 'longword', 'longword',
                    'longword', 'longword', 'longword', 'longword', 'longword',
                ],
                [
                    "Original: ['longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword']",
                    "Long words: ['longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword', 'longword']",
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

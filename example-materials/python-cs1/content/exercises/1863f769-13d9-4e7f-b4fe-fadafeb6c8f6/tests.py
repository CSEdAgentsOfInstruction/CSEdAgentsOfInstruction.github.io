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

    def test_summarizes_example(self):
        self.assert_program(
            [5, 'code', 'planet', 'sun', 'loops', 'program'],
            ['Words with at least 5 characters: 3'],
        )

    def test_handles_empty_and_single_lists(self):
        cases = [
            ([0], ['Words with at least 5 characters: 0']),
            ([1, 'a'], ['Words with at least 5 characters: 0']),
            ([1, 'code'], ['Words with at least 5 characters: 0']),
            ([1, 'loops'], ['Words with at least 5 characters: 1']),
            ([1, 'planet'], ['Words with at least 5 characters: 1']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_checks_lengths_below_at_and_above_five(self):
        cases = [
            ([3, 'code', 'loops', 'planet'], ['Words with at least 5 characters: 2']),
            ([3, 'planet', 'loops', 'code'], ['Words with at least 5 characters: 2']),
            ([3, 'four', 'fives', 'four'], ['Words with at least 5 characters: 1']),
            ([3, 'planet', 'a', 'comet'], ['Words with at least 5 characters: 2']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_all_and_no_matches(self):
        cases = [
            ([4, 'a', 'to', 'sun', 'code'], ['Words with at least 5 characters: 0']),
            (
                [4, 'comet', 'PLANET', 'program', 'house'],
                ['Words with at least 5 characters: 4'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_finds_matches_at_every_position(self):
        for position in range(5):
            words = ['sun', 'sun', 'sun', 'sun', 'sun']
            words[position] = 'comet'
            with self.subTest(matching_position=position):
                self.assert_program([5, *words], ['Words with at least 5 characters: 1'])

    def test_counts_repetitions_and_checks_the_whole_word(self):
        cases = [
            ([5, 'sun', 'comet', 'sun', 'comet', 'planet'], ['Words with at least 5 characters: 3']),
            ([20, *(['program'] * 20)], ['Words with at least 5 characters: 20']),
            ([4, 'b', 'book', 'books', 'bookkeeper'], ['Words with at least 5 characters: 2']),
            ([2, 'abracadabra' * 8, 'bee'], ['Words with at least 5 characters: 1']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

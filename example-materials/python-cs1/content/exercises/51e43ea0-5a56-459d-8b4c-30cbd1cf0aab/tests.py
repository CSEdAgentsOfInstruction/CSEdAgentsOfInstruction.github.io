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
            ['Total characters: 25'],
        )

    def test_handles_empty_and_single_lists(self):
        cases = [
            ([0], ['Total characters: 0']),
            ([1, 'a'], ['Total characters: 1']),
            ([1, 'code'], ['Total characters: 4']),
            ([1, 'loops'], ['Total characters: 5']),
            ([1, 'planet'], ['Total characters: 6']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_processes_every_word_position(self):
        for position in range(5):
            words = ['a', 'a', 'a', 'a', 'a']
            words[position] = 'planet'
            with self.subTest(long_word_position=position):
                self.assert_program([5, *words], ['Total characters: 10'])

    def test_uses_actual_lengths_of_different_words(self):
        cases = [
            ([3, 'an', 'program', 'I'], ['Total characters: 10']),
            ([3, 'a', 'puzzling', 'map'], ['Total characters: 12']),
            ([4, 'a', 'an', 'arch', 'archway'], ['Total characters: 14']),
            ([4, 'code', 'loops', 'planet', 'comet'], ['Total characters: 20']),
            (
                [6, 'a', 'to', 'the', 'code', 'loops', 'planet'],
                ['Total characters: 21'],
            ),
            ([2, 'abracadabra' * 8, 'bee'], ['Total characters: 91']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_counts_repeated_words_each_time(self):
        cases = [
            ([3, 'code', 'code', 'code'], ['Total characters: 12']),
            ([5, 'sun', 'comet', 'sun', 'comet', 'planet'], ['Total characters: 22']),
            ([20, *(['program'] * 20)], ['Total characters: 140']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

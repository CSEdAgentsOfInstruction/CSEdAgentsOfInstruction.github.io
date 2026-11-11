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

    def test_highlights_only_vowels(self):
        cases = [
            (['education'], ['EdUcAtIOn']),
            (['  Programming  '], ['prOgrAmmIng']),
            (['\tEducation\t'], ['EdUcAtIOn']),
            (['AEon'], ['AEOn']),
            (['rhythm'], ['rhythm']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_single_words(self):
        cases = [
            ([''], ['']),
            (['  '], ['']),
            (['a'], ['A']),
            (['Z'], ['z']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_retains_every_character(self):
        cases = [
            (
                [
                    'aeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiouaeiou',
                ],
                [
                    'AEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOU',
                ],
            ),
            (['b1-a e'], ['b1-A E']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

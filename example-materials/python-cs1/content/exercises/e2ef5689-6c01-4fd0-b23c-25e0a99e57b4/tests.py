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

    def test_preserves_order_case_and_repetitions(self):
        cases = [
            (['sun'], ['s', 'u', 'n']),
            (['book'], ['b', 'o', 'o', 'k']),
            (['Sun'], ['S', 'u', 'n']),
            (['  A1b  '], ['A', '1', 'b']),
            (['\tSun\t'], ['S', 'u', 'n']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_single_and_empty_words(self):
        cases = [
            (['x'], ['x']),
            ([''], []),
            (['   '], []),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_internal_spaces_and_long_words(self):
        cases = [
            (['a a'], ['a', ' ', 'a']),
            (['ääÖ'], ['ä', 'ä', 'Ö']),
            (
                [
                    'letterletterletterletterletterletterletterletterletterletterletterletter',
                ],
                [
                    'l', 'e', 't', 't', 'e', 'r', 'l', 'e', 't', 't', 'e', 'r', 'l',
                    'e', 't', 't', 'e', 'r', 'l', 'e', 't', 't', 'e', 'r', 'l', 'e',
                    't', 't', 'e', 'r', 'l', 'e', 't', 't', 'e', 'r', 'l', 'e', 't',
                    't', 'e', 'r', 'l', 'e', 't', 't', 'e', 'r', 'l', 'e', 't', 't',
                    'e', 'r', 'l', 'e', 't', 't', 'e', 'r', 'l', 'e', 't', 't', 'e',
                    'r', 'l', 'e', 't', 't', 'e', 'r',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

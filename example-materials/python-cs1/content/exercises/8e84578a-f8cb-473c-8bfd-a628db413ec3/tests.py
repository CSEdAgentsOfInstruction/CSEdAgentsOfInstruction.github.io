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

    def test_announces_five_different_messages(self):
        cases = [
            (
                ['Welcome', 'Get ready', 'Set', 'Code', 'Celebrate'],
                [
                    'MESSAGE 1: WELCOME', 'MESSAGE 2: GET READY', 'MESSAGE 3: SET',
                    'MESSAGE 4: CODE', 'MESSAGE 5: CELEBRATE',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_announces_each_message_before_reading_the_next(self):
        messages = ['First', '  next  ', '', 'Go!', 'Last']
        reads = []

        def before_input(output):
            expected = [f'MESSAGE {number}: {message.upper()}'
                        for number, message in enumerate(messages[:len(reads)], start=1)]
            self.assertEqual(output, ''.join(line + '\n' for line in expected),
                             'Announce each message before reading the next. '
                             'Put the print inside the input loop.')
            reads.append(len(reads))

        result = run_script(SCRIPT_PATH, input='\n'.join(messages) + '\n',
                            before_input=before_input)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(reads), 5, 'Read exactly five messages.')
        expected = [f'MESSAGE {number}: {message.upper()}'
                    for number, message in enumerate(messages, start=1)]
        self.assertEqual(result.stdout, ''.join(line + '\n' for line in expected),
                         'Print only the five announcements.')

    def test_keeps_repeated_messages(self):
        cases = [
            (
                ['same', 'same', 'same', 'same', 'same'],
                [
                    'MESSAGE 1: SAME', 'MESSAGE 2: SAME', 'MESSAGE 3: SAME',
                    'MESSAGE 4: SAME', 'MESSAGE 5: SAME',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_messages(self):
        cases = [
            (
                ['', ' ', 'two words', 'a1', 'end'],
                [
                    'MESSAGE 1: ', 'MESSAGE 2:  ', 'MESSAGE 3: TWO WORDS',
                    'MESSAGE 4: A1', 'MESSAGE 5: END',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_whitespace_and_punctuation(self):
        cases = [
            (
                ['  padded  ', 'MIXED case', '\tTab', 'Ää', 'Finish!'],
                [
                    'MESSAGE 1:   PADDED  ', 'MESSAGE 2: MIXED CASE',
                    'MESSAGE 3: \tTAB', 'MESSAGE 4: ÄÄ', 'MESSAGE 5: FINISH!',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

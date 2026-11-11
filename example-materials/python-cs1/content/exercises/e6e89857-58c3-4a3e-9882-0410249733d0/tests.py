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

    def test_stops_immediately(self):
        cases = [
            (['done'], ['Sessions: 0', 'Total pages: 0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_normalizes_immediate_done(self):
        cases = [
            ([' DONE '], ['Sessions: 0', 'Total pages: 0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_summarizes_example_sessions(self):
        cases = [
            (['12', '20', '15', 'done'], ['Sessions: 3', 'Total pages: 47']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_counts_zero_page_sessions(self):
        cases = [
            (['0', '9', '0', 'Done'], ['Sessions: 3', 'Total pages: 9']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_many_sessions(self):
        cases = [
            (
                [
                    '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5',
                    '5', '5', '5', '5', '5', '5', '5', 'done',
                ],
                ['Sessions: 20', 'Total pages: 100'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_ignores_later_input(self):
        cases = [
            (['7', 'done', '99'], ['Sessions: 1', 'Total pages: 7']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

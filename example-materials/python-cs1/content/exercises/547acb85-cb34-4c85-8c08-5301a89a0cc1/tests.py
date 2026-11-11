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

    def test_replaces_example_middle_item(self):
        cases = [
            (['red', 'green', 'blue', 'yellow'], ["['red', 'yellow', 'blue']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_uses_new_input_values(self):
        cases = [
            (['black', 'white', 'orange', 'purple'], ["['black', 'purple', 'orange']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_replaces_only_one_of_repeated_values(self):
        cases = [
            (['red', 'red', 'red', 'blue'], ["['red', 'blue', 'red']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_multiword_colors(self):
        cases = [
            (
                ['dark red', 'light green', 'deep blue', 'pale gold'],
                ["['dark red', 'pale gold', 'deep blue']"],
            ),
            (
                [' red ', 'green', ' blue ', ' gold '],
                ["[' red ', ' gold ', ' blue ']"],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_allows_an_unchanged_value(self):
        cases = [
            (['red', 'green', 'blue', 'green'], ["['red', 'green', 'blue']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

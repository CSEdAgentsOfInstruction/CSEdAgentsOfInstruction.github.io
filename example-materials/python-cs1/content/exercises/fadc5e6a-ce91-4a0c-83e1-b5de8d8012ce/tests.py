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

    def test_inspects_example_cities(self):
        cases = [
            (
                ['Helsinki', 'Oslo', 'Tallinn', 'Reykjavik'],
                [
                    "Cities: ['Helsinki', 'Oslo', 'Tallinn', 'Reykjavik']",
                    'First: Helsinki', 'Last: Reykjavik', 'Number of cities: 4',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_uses_entered_city_names(self):
        cases = [
            (
                ['Paris', 'Rome', 'Lima', 'Tokyo'],
                [
                    "Cities: ['Paris', 'Rome', 'Lima', 'Tokyo']",
                    'First: Paris', 'Last: Tokyo', 'Number of cities: 4',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_keeps_multiword_names(self):
        cases = [
            (
                ['New York', 'Cape Town', "St. John's", 'São Paulo'],
                [
                    'Cities: [\'New York\', \'Cape Town\', "St. John\'s", \'São Paulo\']',
                    'First: New York', 'Last: São Paulo', 'Number of cities: 4',
                ],
            ),
            (
                [' Oslo ', 'Rome', 'Lima', ' Tokyo '],
                [
                    "Cities: [' Oslo ', 'Rome', 'Lima', ' Tokyo ']",
                    'First:  Oslo ', 'Last:  Tokyo ', 'Number of cities: 4',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_repeated_and_short_names(self):
        cases = [
            (
                ['A', 'A', 'A', 'A'],
                [
                    "Cities: ['A', 'A', 'A', 'A']",
                    'First: A', 'Last: A', 'Number of cities: 4',
                ],
            ),
            (
                ['Oslo', 'Lima', 'Oslo', 'Rome'],
                [
                    "Cities: ['Oslo', 'Lima', 'Oslo', 'Rome']",
                    'First: Oslo', 'Last: Rome', 'Number of cities: 4',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

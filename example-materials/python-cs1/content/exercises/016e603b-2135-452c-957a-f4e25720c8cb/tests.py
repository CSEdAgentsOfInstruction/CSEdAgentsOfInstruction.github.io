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

    def test_splits_at_commas(self):
        cases = [
            (
                ['oxygen tanks, repair kit, water'],
                ['Item count: 3', 'oxygen tanks', 'repair kit', 'water'],
            ),
            (
                ['tools,fuel cells,medical supplies'],
                ['Item count: 3', 'tools', 'fuel cells', 'medical supplies'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_strips_only_surrounding_whitespace(self):
        cases = [
            (
                ['  solar sail  ,  spare cable ,food packs '],
                ['Item count: 3', 'solar sail', 'spare cable', 'food packs'],
            ),
            (['\tfirst\t, second  '], ['Item count: 2', 'first', 'second']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_one_item_and_duplicates(self):
        cases = [
            (['navigation computer'], ['Item count: 1', 'navigation computer']),
            (['water,water,water'], ['Item count: 3', 'water', 'water', 'water']),
            (['a,b'], ['Item count: 2', 'a', 'b']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_many_items(self):
        cases = [
            (
                [
                    'item 0,item 1,item 2,item 3,item 4,item 5,item 6,item 7,item 8,item 9,item 10,item 11,item 12,item 13,item 14,item 15,item 16,item 17,item 18,item 19',
                ],
                [
                    'Item count: 20', 'item 0', 'item 1', 'item 2', 'item 3', 'item 4',
                    'item 5', 'item 6', 'item 7', 'item 8', 'item 9', 'item 10',
                    'item 11', 'item 12', 'item 13', 'item 14', 'item 15', 'item 16',
                    'item 17', 'item 18', 'item 19',
                ],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_case_and_whitespace_inside_names(self):
        cases = [
            (['Water, OXYGEN Tanks'], ['Item count: 2', 'Water', 'OXYGEN Tanks']),
            (['  oxygen  tanks ,water'], ['Item count: 2', 'oxygen  tanks', 'water']),
            (['\tSpare\tCable\t,  Repair   Kit  '],
             ['Item count: 2', 'Spare\tCable', 'Repair   Kit']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

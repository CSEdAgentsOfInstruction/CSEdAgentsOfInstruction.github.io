# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_code, run_script
import json
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


STATE_RUNNER = r'''
import contextlib
import io
import json
import os
import runpy
import sys

script_path = os.path.abspath(sys.argv[1])
observed = []

def remember_lists(frame, event, result):
    # Observe executed values, without reading or inspecting student source.
    # A function wrapper is allowed: its final local values count too.
    if event == "return" and frame.f_globals.get("__file__") == script_path:
        names = dict(frame.f_globals)
        names.update(frame.f_locals)
        if "titles" in names and "matching_titles" in names:
            observed.append((names["titles"], names["matching_titles"]))

output = io.StringIO()
with contextlib.redirect_stdout(output):
    sys.setprofile(remember_lists)
    try:
        try:
            runpy.run_path(script_path, run_name="__main__")
        except SystemExit as error:
            if error.code not in (None, 0):
                raise
    finally:
        sys.setprofile(None)

state = {"output": output.getvalue(), "lists": []}
for titles, matching_titles in observed:
    # Keep each scope's final objects. An unused global starter variable must
    # not hide the result constructed and printed inside a function.
    state["lists"].append({
        "titles": titles if isinstance(titles, list) else None,
        "matches": matching_titles if isinstance(matching_titles, list) else None,
        "separate": titles is not matching_titles,
    })
print(json.dumps(state))
'''


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

    def test_searches_example_archive(self):
        cases = [
            (
                [
                    4, 'The Night Train', 'Signals at Dawn', 'Midnight Code',
                    'The Last Map', 'night',
                ],
                ["Matches: ['The Night Train', 'Midnight Code']"],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_and_single_archives(self):
        cases = [
            ([0, 'night'], ['Matches: []']),
            ([1, 'Atlas', 'night'], ['Matches: []']),
            ([1, 'Night', 'NIGHT'], ["Matches: ['Night']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_ignores_case_and_uses_search_term(self):
        cases = [
            (
                [3, 'NIGHT WATCH', 'Daylight', 'Late Night', 'NiGhT'],
                ["Matches: ['NIGHT WATCH', 'Late Night']"],
            ),
            ([3, 'Map', 'MAP Room', 'Atlas', 'map'], ["Matches: ['Map', 'MAP Room']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_order_spelling_and_repetitions(self):
        cases = [
            (
                [3, 'Night', 'Night', 'MIDNIGHT', 'night'],
                ["Matches: ['Night', 'Night', 'MIDNIGHT']"],
            ),
            (
                [3, "Ada's Map", 'The Map Room', 'MAPPING', 'map'],
                ['Matches: ["Ada\'s Map", \'The Map Room\', \'MAPPING\']'],
            ),
            (
                [2, ' Night ', 'NIGHT ', 'night'],
                ["Matches: [' Night ', 'NIGHT ']"],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_term_and_longer_archive(self):
        cases = [
            ([2, 'Alpha', 'Beta', ''], ["Matches: ['Alpha', 'Beta']"]),
            (
                [
                    21, 'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word',
                    'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word',
                    'word', 'word', 'word', 'word', 'Last Match', 'last',
                ],
                ["Matches: ['Last Match']"],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_spaces_in_the_search_term(self):
        cases = [
            ([2, 'Midnight Code', 'A night train', ' night '],
             ["Matches: ['A night train']"]),
            ([3, 'Night Train', 'Midnight', 'A NIGHT WALK', 'NiGhT '],
             ["Matches: ['Night Train', 'A NIGHT WALK']"]),
            ([3, 'Night', 'Night Train', 'Two  Spaces', ' '],
             ["Matches: ['Night Train', 'Two  Spaces']"]),
            ([2, 'One space', 'Two  Spaces', '  '],
             ["Matches: ['Two  Spaces']"]),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_archive_and_builds_a_separate_list(self):
        cases = [
            ([], 'night'),
            ([], ''),
            (['Night'], 'NIGHT'),
            (['Atlas'], 'night'),
            (['Night', 'Night', 'MIDNIGHT'], 'night'),
            (['Alpha', '', 'Beta', 'Alpha'], ''),
            (['The Night Train', 'Signals at Dawn', 'Midnight Code'], 'night'),
            ([' Night ', 'MIDNIGHT', 'A NIGHT WALK'], ' night '),
            (['Ää', 'ÄÄ', "Ada's Map", ''], 'ä'),
        ]
        for titles, term in cases:
            with self.subTest(titles=titles, term=term):
                entered = [str(len(titles)), *titles, term]
                try:
                    result = run_code(STATE_RUNNER, input='\n'.join(entered) + '\n', argv=[SCRIPT_PATH])
                except TimeoutError:
                    self.fail('The search must finish for this archive and term.')
                self.assertEqual(
                    result.returncode, 0,
                    f'The program must finish successfully:\n{result.stderr}',
                )
                state = json.loads(result.stdout)
                expected = [title for title in titles if term.lower() in title.lower()]
                self.assertEqual(
                    state['output'].splitlines(), [f'Matches: {expected}'],
                    'Print only the matching titles in their original form.',
                )
                self.assertTrue(
                    state['lists'],
                    'Keep the original titles in titles and the result in matching_titles.',
                )
                stored_lists = [
                    item for item in state['lists']
                    if item['titles'] is not None and item['matches'] is not None
                ]
                self.assertTrue(
                    stored_lists,
                    'Both titles and matching_titles must contain lists.',
                )
                preserved = [item for item in stored_lists if item['titles'] == titles]
                self.assertTrue(
                    preserved,
                    'Leave titles unchanged, including spelling, order, and repetitions.',
                )
                correct_results = [item for item in preserved if item['matches'] == expected]
                self.assertTrue(
                    correct_results,
                    'Store every matching original title in matching_titles.',
                )
                self.assertTrue(
                    any(item['separate'] for item in correct_results),
                    'Build a separate matching_titles list, even when all or no titles match.',
                )


if __name__ == "__main__":
    unittest.main()

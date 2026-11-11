# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestProgram(unittest.TestCase):
    def test_uses_a_direct_loop_over_word(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                tree = ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"The program must contain valid Python. Python reported: {error}")

        self.assertTrue(
            any(
                isinstance(node, ast.For)
                and isinstance(node.iter, ast.Name)
                and node.iter.id == "word"
                for node in ast.walk(tree)
            ),
            "Use a direct 'for ... in word' loop to inspect and count the vowels.",
        )

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

    def test_counts_every_match(self):
        cases = [
            (['banana'], ['3']),
            (['abracadabra'], ['5']),
            (['  Aardvark  '], ['3']),
            (['ÄÖaeiou'], ['5']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_words_and_no_matches(self):
        cases = [
            (['rhythm'], ['0']),
            (['käpy'], ['0']),
            ([''], ['0']),
            (['   '], ['0']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_single_letters_and_long_words(self):
        cases = [
            (['a'], ['1']),
            (['Z'], ['0']),
            (['AEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOU'], ['60']),
            (['aZZZaZZZa'], ['3']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

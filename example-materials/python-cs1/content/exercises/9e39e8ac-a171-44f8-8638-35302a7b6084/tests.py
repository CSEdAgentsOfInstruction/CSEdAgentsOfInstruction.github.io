# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestProgram(unittest.TestCase):
    def test_uses_indexes_and_len(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                tree = ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"The program must contain valid Python. Python reported: {error}")

        word_indexes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id == "word"
            and not isinstance(node.slice, ast.Slice)
        ]
        self.assertGreaterEqual(
            len(word_indexes),
            2,
            "Use square-bracket indexes on word to find both the first and last character.",
        )
        self.assertTrue(
            any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "len"
                and node.args
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id == "word"
                for node in ast.walk(tree)
            ),
            "Use len(word) to find the length.",
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

    def test_inspects_different_words(self):
        cases = [
            (['python'], ['First: p', 'Last: n', 'Length: 6']),
            (['Ada'], ['First: A', 'Last: a', 'Length: 3']),
            (['planet'], ['First: p', 'Last: t', 'Length: 6']),
            (['käsi'], ['First: k', 'Last: i', 'Length: 4']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_one_character(self):
        cases = [
            (['x'], ['First: x', 'Last: x', 'Length: 1']),
            (['A'], ['First: A', 'Last: A', 'Length: 1']),
            (['Ö'], ['First: Ö', 'Last: Ö', 'Length: 1']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_preserves_case_and_repetitions(self):
        cases = [
            (['AAa'], ['First: A', 'Last: a', 'Length: 3']),
            (['bookkeeper'], ['First: b', 'Last: r', 'Length: 10']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_longer_words(self):
        cases = [
            (
                ['abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc'],
                ['First: a', 'Last: c', 'Length: 60'],
            ),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

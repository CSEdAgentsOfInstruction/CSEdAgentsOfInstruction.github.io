# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestProgram(unittest.TestCase):
    def read_tree(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                return ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"The program must contain valid Python. Python reported: {error}")

    def test_uses_the_requested_counter_pattern(self):
        tree = self.read_tree()
        direct_loops = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.For)
            and isinstance(node.iter, ast.Name)
            and node.iter.id == "word"
        ]
        self.assertTrue(
            direct_loops,
            "Keep a direct for loop over word so every character is inspected.",
        )
        loop = direct_loops[0]

        def assigns_zero_to_count(node):
            if isinstance(node, ast.Assign):
                assigns_count = any(
                    isinstance(target, ast.Name) and target.id == "count"
                    for target in node.targets
                )
                value = node.value
            elif isinstance(node, ast.AnnAssign):
                assigns_count = (
                    isinstance(node.target, ast.Name) and node.target.id == "count"
                )
                value = node.value
            else:
                return False
            return (
                assigns_count
                and isinstance(value, ast.Constant)
                and value.value == 0
            )

        loop_nodes = set(ast.walk(loop))
        self.assertTrue(
            any(
                node not in loop_nodes
                and getattr(node, "lineno", loop.lineno) < loop.lineno
                and assigns_zero_to_count(node)
                for node in ast.walk(tree)
            ),
            "Initialize count to 0 once before the character loop.",
        )

        def updates_count(node):
            if isinstance(node, ast.Assign):
                return any(
                    isinstance(target, ast.Name) and target.id == "count"
                    for target in node.targets
                )
            if isinstance(node, ast.AnnAssign):
                return isinstance(node.target, ast.Name) and node.target.id == "count"
            return (
                isinstance(node, ast.AugAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == "count"
            )

        self.assertTrue(
            any(
                updates_count(descendant)
                for condition in loop.body
                if isinstance(condition, ast.If)
                for descendant in ast.walk(condition)
            ),
            "Update count inside the condition in the character loop.",
        )

    def test_normalizes_with_strip_and_lower(self):
        tree = self.read_tree()
        called_methods = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertTrue(
            {"strip", "lower"}.issubset(called_methods),
            "Normalize the entered word with both .strip() and .lower().",
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
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)

    def test_handles_empty_words_and_no_matches(self):
        cases = [
            (['rhythm'], ['0']),
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
            (['AEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOUAEIOU'], ['12']),
            (['aZZZaZZZa'], ['3']),
        ]
        for entered, expected in cases:
            with self.subTest(entered=entered):
                self.assert_program(entered, expected)


if __name__ == "__main__":
    unittest.main()

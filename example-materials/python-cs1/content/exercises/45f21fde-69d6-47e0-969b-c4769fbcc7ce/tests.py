# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestPassOrNotYet(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_uses_if_else(self):
        with open(self.script_path(), encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        if_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.If)]
        self.assertTrue(if_nodes, "Use an if statement.")
        self.assertTrue(if_nodes[0].orelse, "Use else for the alternative outcome.")

    def test_score_boundaries(self):
        cases = [(0, "Not yet"), (69, "Not yet"), (70, "Pass"), (71, "Pass"), (100, "Pass")]
        for score, expected in cases:
            with self.subTest(score=score):
                result = run_script(self.script_path(), input=f'{score}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip(),
                    expected,
                    f"For a score of {score}, print exactly {expected!r}. Remember "
                    "that 70 belongs to the passing range.",
                )


if __name__ == "__main__":
    unittest.main()

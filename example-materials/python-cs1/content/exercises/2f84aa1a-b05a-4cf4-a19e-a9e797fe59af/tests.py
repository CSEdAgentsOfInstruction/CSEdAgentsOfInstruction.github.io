# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import ast
import os
import sys
import unittest


class TestImprovedNames(unittest.TestCase):
    def test_uses_the_requested_names(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        with open(script_path, encoding="utf-8") as source_file:
            tree = ast.parse(source_file.read())

        names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        self.assertTrue(
            {"course_name", "student_name", "room"}.issubset(names),
            "Use course_name, student_name, and room throughout the program.",
        )
        for old_name in ["a", "b", "c"]:
            self.assertNotIn(
                old_name,
                names,
                f"Replace the unclear variable name {old_name!r} everywhere.",
            )

    def test_preserves_the_program_behavior(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        cases = [
            ("Programming", "Ada", "A123"),
            ("Data Science", "Grace", "B204"),
        ]
        for course_name, student_name, room in cases:
            with self.subTest(student_name=student_name):
                result = run_script(script_path, input=f'{course_name}\n{student_name}\n{room}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertIn("Course name: ", result.stdout)
                self.assertIn("Student name: ", result.stdout)
                self.assertIn("Room: ", result.stdout)
                self.assertTrue(
                    result.stdout.rstrip().endswith(
                        f"{student_name} has {course_name} in {room}."
                    ),
                    "Keep the original final sentence and insert all three entered values.",
                )


if __name__ == "__main__":
    unittest.main()

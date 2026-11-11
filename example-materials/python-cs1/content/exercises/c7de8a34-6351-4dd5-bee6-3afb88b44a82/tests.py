# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import time_limit
import ast
import contextlib
import io
import os
import runpy
import sys
import time
import unittest
from unittest.mock import patch


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")





class TestCalculationChecks(unittest.TestCase):
    def test_uses_assert_statements(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                tree = ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"The program must contain valid Python. Python reported: {error}")

        self.assertTrue(
            any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "Use assert statements to check triple's results for positive, zero, and negative inputs.",
        )

    def run_script(self, replacement=None):
        output = io.StringIO()
        errors = io.StringIO()
        observed = 0
        substituted = False
        failure = None
        namespace = {}
        previous_profile = sys.getprofile()

        with contextlib.ExitStack() as patches:
            def observe(frame, event, argument):
                nonlocal observed, substituted
                check = frame.f_globals.get("check_triple")
                if event == "call" and getattr(check, "__code__", None) is frame.f_code:
                    observed += 1
                    if replacement is not None and not substituted:
                        original = frame.f_globals.get("triple")
                        if callable(original):
                            # Replace aliases too, without prescribing the student's call spelling.
                            replacements = {
                                name: replacement for name, value in frame.f_globals.items()
                                if value is original
                            }
                            patches.enter_context(patch.dict(frame.f_globals, replacements))
                            substituted = True

            try:
                sys.setprofile(observe)
                with time_limit(), contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    with patch("builtins.input", side_effect=RuntimeError("The checks should not ask for input.")):
                        namespace = runpy.run_path(SCRIPT_PATH, run_name="__main__")
            except BaseException as error:
                failure = error
            finally:
                sys.setprofile(previous_profile)

        self.assertEqual(output.getvalue(), "", "Passing checks should be silent. Remove printed messages.")
        self.assertEqual(errors.getvalue(), "", "The checks should not write error messages.")
        self.assertGreater(observed, 0, "Keep the call that runs check_triple after the definitions.")
        return namespace, failure

    def assert_success(self, failure):
        self.assertIsNone(failure, f"The checks should pass for a correct calculation, but raised {failure!r}.")

    def test_supplied_calculation_still_matches_its_rule(self):
        namespace, failure = self.run_script()
        self.assert_success(failure)
        calculation = namespace.get("triple")
        self.assertTrue(callable(calculation), "Keep the supplied triple(number) function.")
        for number in (0, 1, -1, 7, -12, 38, -41):
            with self.subTest(number=number):
                output = io.StringIO()
                with time_limit(), contextlib.redirect_stdout(output):
                    with patch("builtins.input", side_effect=RuntimeError("The calculation should not ask for input.")):
                        result = calculation(number=number)
                self.assertEqual(result, number * 3, "triple should return three times its argument.")
                self.assertEqual(output.getvalue(), "", "triple should return its result without printing.")

    def test_running_the_program_executes_passing_checks(self):
        _, failure = self.run_script()
        self.assert_success(failure)

    def test_checks_accept_equivalent_correct_calculations(self):
        def repeated_addition(number):
            return number + number + number

        def mixed_operations(number):
            return number * 2 + number

        for correct in (repeated_addition, mixed_operations):
            with self.subTest(implementation=correct.__name__):
                _, failure = self.run_script(correct)
                self.assert_success(failure)

    def test_checks_expose_wrong_results_in_each_input_category(self):
        categories = (
            ("a positive integer", lambda number: number > 0),
            ("zero", lambda number: number == 0),
            ("a negative integer", lambda number: number < 0),
        )
        for description, in_category in categories:
            for difference in (-1, 1):
                def faulty(number):
                    result = number * 3
                    if isinstance(number, int) and not isinstance(number, bool) and in_category(number):
                        result += difference
                    return result

                with self.subTest(category=description, difference=difference):
                    _, failure = self.run_script(faulty)
                    self.assertIsInstance(
                        failure, AssertionError,
                        f"Your assertions did not expose an incorrect result for {description}. "
                        "Check a call using that kind of input against its expected result.",
                    )


if __name__ == "__main__":
    unittest.main()

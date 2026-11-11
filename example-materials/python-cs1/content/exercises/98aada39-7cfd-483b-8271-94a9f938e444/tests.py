# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script, time_limit
import ast
import contextlib
import importlib.util
import io
import os
import sys
import unittest
from unittest.mock import Mock, patch


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")





class BehaviorTest(unittest.TestCase):
    FUNCTIONS = ()
    LOAD_INPUTS = ()
    ALLOW_STARTUP_OUTPUT = False

    def setUp(self):
        spec = importlib.util.spec_from_file_location("student_solution", SCRIPT_PATH)
        self.module = importlib.util.module_from_spec(spec)
        output = io.StringIO()
        with time_limit(), patch("builtins.input", side_effect=self.LOAD_INPUTS), contextlib.redirect_stdout(output):
            spec.loader.exec_module(self.module)
        self.startup_output = output.getvalue()
        if not self.ALLOW_STARTUP_OUTPUT:
            self.assertEqual(self.startup_output, "", "Keep displayed output in the part of the program responsible for presentation.")
        for name in self.FUNCTIONS:
            self.assertTrue(callable(getattr(self.module, name, None)), f"Define the function {name} from the handout.")

    def call(self, name, *args):
        output = io.StringIO()
        with time_limit(), contextlib.redirect_stdout(output):
            result = getattr(self.module, name)(*args)
        return result, output.getvalue()

    def calculation(self, name, *args):
        result, output = self.call(name, *args)
        self.assertEqual(output, "", f"{name} should return its result without printing.")
        return result

    def run_program(self, responses=()):
        completed = run_script(SCRIPT_PATH, input='\n'.join(responses) + ('\n' if responses else ''))
        self.assertEqual(completed.returncode, 0, "The complete program must finish successfully.\n" + completed.stderr)
        self.assertEqual(completed.stderr, "", "The program should not write errors.")
        return completed.stdout

    def run_and_observe_calls(self, names, responses=()):
        import runpy

        observed = {name: 0 for name in names}
        previous_profile = sys.getprofile()

        def observe(frame, event, arg):
            if event == "call":
                for name in names:
                    function = frame.f_globals.get(name)
                    if getattr(function, "__code__", None) is frame.f_code:
                        observed[name] += 1

        output = io.StringIO()
        try:
            sys.setprofile(observe)
            with time_limit(), patch("builtins.input", side_effect=responses), contextlib.redirect_stdout(output):
                runpy.run_path(SCRIPT_PATH, run_name="__main__")
        finally:
            sys.setprofile(previous_profile)
        return output.getvalue(), observed

    def read(self, name, responses, *args):
        reader = Mock(side_effect=responses)
        with patch("builtins.input", reader):
            result, output = self.call(name, *args)
        return result, output, reader


class TestDisplay(BehaviorTest):
    FUNCTIONS = ('show_status',)
    ALLOW_STARTUP_OUTPUT = True

    def test_keeps_one_function_definition_and_call(self):
        with open(SCRIPT_PATH, encoding="utf-8") as source_file:
            try:
                tree = ast.parse(source_file.read())
            except SyntaxError as error:
                self.fail(f"Repair the function-definition syntax. Python reported: {error}")

        definitions = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "show_status"
        ]
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "show_status"
        ]
        self.assertEqual(
            len(definitions),
            1,
            "Repair the existing show_status definition instead of adding another definition.",
        )
        self.assertEqual(
            len(calls),
            1,
            "Keep the existing single show_status() call.",
        )

    def test_program_calls_the_display_function(self):
        output, observed = self.run_and_observe_calls({'show_status'})
        self.assertEqual(observed['show_status'], 1, "Use the display function for the required calls in the complete program.")

    def test_complete_display(self):
        self.assertEqual(
            self.run_program(),
            'ONLINE\n',
            "The complete program should print exactly one ONLINE line.",
        )

    def test_function_can_be_called_independently(self):
        result, output = self.call('show_status')
        self.assertEqual(output, 'ONLINE\n', "Keep the display in the function so another caller can use it.")

    def test_repeated_calls_produce_complete_displays(self):
        for attempt in range(3):
            with self.subTest(attempt=attempt):
                result, output = self.call('show_status')
                self.assertEqual(
                    output,
                    'ONLINE\n',
                    "Each show_status call should print one complete ONLINE line.",
                )


if __name__ == "__main__":
    unittest.main()

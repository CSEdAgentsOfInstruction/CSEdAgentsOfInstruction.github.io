# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script, time_limit
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

    def read(self, name, responses, *args):
        reader = Mock(side_effect=responses)
        with patch("builtins.input", reader):
            result, output = self.call(name, *args)
        return result, output, reader


class TestSearch(BehaviorTest):
    FUNCTIONS = ("contains_signal",)

    def check_case(self, messages, signal, expected):
        original = list(messages)
        result = self.calculation("contains_signal", messages, signal)
        self.assertIs(result, expected, "Return True for an exact match anywhere, otherwise False.")
        self.assertEqual(messages, original, "Searching must leave messages unchanged.")

    def test_matches_at_each_position(self):
        for signal in ["echo", "ready", "new signal"]:
            for index in range(4):
                messages = ["other"] * 4
                messages[index] = signal
                with self.subTest(signal=signal, index=index): self.check_case(messages, signal, True)

    def test_empty_single_and_absent(self):
        for messages, signal, expected in [([], "echo", False), (["echo"], "echo", True), (["clear"], "echo", False), (["echo", "echo"], "ready", False)]:
            with self.subTest(messages=messages): self.check_case(messages, signal, expected)

    def test_exact_text_and_repeated_matches(self):
        for messages, signal, expected in [(["ECHO", "echoes"], "echo", False), ([" echo "], "echo", False), (["e"], "echo", False), ([""], "echo", False), (["echo"], "", False), ([""], "", True), (["x", "echo", "echo"], "echo", True)]:
            with self.subTest(messages=messages): self.check_case(messages, signal, expected)


if __name__ == "__main__":
    unittest.main()

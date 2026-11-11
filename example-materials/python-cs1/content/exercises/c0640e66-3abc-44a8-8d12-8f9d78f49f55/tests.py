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


class TestReadingTracker(BehaviorTest):
    FUNCTIONS = ("read_sessions", "total_minutes", "longest_session", "count_long_sessions", "print_summary", "main")
    PROMPT = "Minutes, or done: "
    ERROR = "Please enter a positive integer or done."

    def check_input(self, responses, expected, error_count):
        result, output, reader = self.read("read_sessions", responses)
        self.assertEqual(result, expected)
        self.assertTrue(all(type(value) is int for value in result))
        self.assertEqual(output.splitlines(), [self.ERROR] * error_count)
        self.assertEqual(reader.call_count, len(responses), "Stop at the sentinel.")
        self.assertTrue(all(call.args == (self.PROMPT,) for call in reader.call_args_list), "Use the requested prompt on each attempt.")

    def test_sentinel_variations_and_immediate_stopping(self):
        for response in ["done", "DONE", "  DoNe\t"]:
            with self.subTest(response=response): self.check_input([response], [], 0)

    def test_invalid_attempts_then_valid_sessions(self):
        self.check_input(["hello", "12.5", "0", "-4", " 12 ", "DONE"], [12], 4)
        self.check_input(["", " ", "+0", "-0", "000", "+0005", "done"], [5], 5)
        self.check_input(["5", "bad", "30", "-1", "45", "5", "done"], [5, 30, 45, 5], 2)

    def test_unexpected_input_failure_is_not_hidden(self):
        with patch("builtins.input", side_effect=[EOFError("input unavailable"), "done"]):
            with self.assertRaises(EOFError): self.call("read_sessions")

    def test_total_and_longest_for_varied_lists(self):
        for sessions in [[], [12], [20, 45, 15], [80, 5, 3], [3, 5, 80], [7, 7, 7], [1000001, 4, 2000002]]:
            with self.subTest(sessions=sessions):
                for name, expected in [("total_minutes", sum(sessions)), ("longest_session", max(sessions) if sessions else 0)]:
                    original = list(sessions)
                    result = self.calculation(name, sessions)
                    self.assertIs(type(result), int)
                    self.assertEqual(result, expected)
                    self.assertEqual(sessions, original)

    def test_count_uses_the_supplied_inclusive_boundary(self):
        for sessions, minimum in [([], 30), ([29, 30, 31], 30), ([30, 44, 45, 60], 45), ([5, 5, 5], 5), ([1, 2], 3), ([1, 2], 1)]:
            with self.subTest(sessions=sessions, minimum=minimum):
                original = list(sessions)
                result = self.calculation("count_long_sessions", sessions, minimum)
                self.assertIs(type(result), int)
                self.assertEqual(result, sum(value >= minimum for value in sessions))
                self.assertEqual(sessions, original)

    def summary(self, sessions):
        longest = max(sessions) if sessions else "none"
        return f"Sessions: {len(sessions)}\nTotal minutes: {sum(sessions)}\nLongest session: {longest}\nLong sessions: {sum(value >= 30 for value in sessions)}\n"

    def test_summary_presents_supplied_values(self):
        for count, total, longest, long_count in [(3, 80, 45, 1), (0, 0, 0, 0), (1, 30, 30, 1), (4, 123, 50, 2)]:
            result, output = self.call("print_summary", count, total, longest, long_count)
            label = longest if count else "none"
            self.assertEqual(output, f"Sessions: {count}\nTotal minutes: {total}\nLongest session: {label}\nLong sessions: {long_count}\n")

    def test_main_connects_the_functions(self):
        sessions = [20, 30, 45]
        with patch.object(self.module, "read_sessions", autospec=True, return_value=sessions) as read, patch.object(self.module, "total_minutes", autospec=True, return_value=101) as total, patch.object(self.module, "longest_session", autospec=True, return_value=62) as longest, patch.object(self.module, "count_long_sessions", autospec=True, return_value=1) as count, patch.object(self.module, "print_summary", autospec=True) as display:
            self.calculation("main")
            read.assert_called_once_with()
            total.assert_any_call(sessions)
            longest.assert_any_call(sessions)
            count.assert_any_call(sessions, 30)
            display.assert_called_once_with(3, 101, 62, 1)

    def test_program_runs_main(self):
        output, observed = self.run_and_observe_calls({"main"}, ["done"])
        self.assertGreater(observed["main"], 0, "Run the program through main so it coordinates the helper functions.")

    def test_complete_program_stops_after_one_summary(self):
        for responses, sessions in [(["done"], []), (["20", "45", "15", "done"], [20, 45, 15]), ([" 30 ", " DoNe "], [30]), (["5", "5", "5", "done"], [5, 5, 5])]:
            with self.subTest(responses=responses):
                self.assertEqual(self.run_program(responses), self.PROMPT * len(responses) + self.summary(sessions))

    def test_complete_program_retries_in_the_right_order(self):
        responses = ["bad", "0", "12", "-1", "30", "DONE"]
        expected = self.PROMPT + self.ERROR + "\n" + self.PROMPT + self.ERROR + "\n" + self.PROMPT + self.PROMPT + self.ERROR + "\n" + self.PROMPT + self.PROMPT + self.summary([12, 30])
        self.assertEqual(self.run_program(responses), expected)


if __name__ == "__main__":
    unittest.main()

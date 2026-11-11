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


class TestTournament(BehaviorTest):
    FUNCTIONS = ("select_finalists", "total_points", "print_shortlist", "main")
    ALLOW_STARTUP_OUTPUT = True

    def test_selection_preserves_order_and_repeated_scores(self):
        cases = [([], 80), ([70, 79], 80), ([80], 80), ([71, 84, 90, 84, 63], 84), ([100, 70, 100, 85], 85), ([0, 0, 1], 0), ([-3, -1, -3], -3)]
        for scores, minimum in cases:
            with self.subTest(scores=scores, minimum=minimum):
                original = list(scores)
                result = self.calculation("select_finalists", scores, minimum)
                self.assertIsInstance(result, list)
                self.assertEqual(result, [score for score in scores if score >= minimum])
                self.assertEqual(scores, original)
                self.assertIsNot(result, scores, "Return a new list even when every score qualifies or the input is empty.")
                result.append(12345)
                self.assertEqual(scores, original, "Changing the returned list must not change scores.")

    def test_totals_for_varied_inputs(self):
        for scores in [[], [84], [84, 90, 84], [0, 5], [2, 2, 2], [-4, 5, -4]]:
            with self.subTest(scores=scores):
                original = list(scores)
                self.assertEqual(self.calculation("total_points", scores), sum(scores))
                self.assertEqual(scores, original)

    def test_presentation_uses_both_supplied_results(self):
        for finalists, total in [([80, 95], 175), ([], 0), ([3, 3], 6), ([3, 3], 20)]:
            with self.subTest(finalists=finalists, total=total):
                original = list(finalists)
                result, output = self.call("print_shortlist", finalists, total)
                self.assertEqual(output, f"Finalists: {finalists}\nCombined points: {total}\n")
                self.assertEqual(finalists, original)

    def test_main_passes_returned_results_to_the_next_function(self):
        finalists = [88, 91]
        with patch.object(self.module, "select_finalists", autospec=True, return_value=finalists) as select, patch.object(self.module, "total_points", autospec=True, return_value=321) as total, patch.object(self.module, "print_shortlist", autospec=True) as display:
            self.calculation("main")
            select.assert_any_call([71, 84, 90, 84, 63], 84)
            total.assert_any_call(finalists)
            display.assert_called_once_with(finalists, 321)

    def test_program_runs_main(self):
        output, observed = self.run_and_observe_calls({"main"}, [])
        self.assertGreater(observed["main"], 0, "Run the program through main so it coordinates the helper functions.")

    def test_complete_program(self):
        self.assertEqual(self.run_program(), "Finalists: [84, 90, 84]\nCombined points: 258\n")


if __name__ == "__main__":
    unittest.main()

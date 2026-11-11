# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestWeatherAdvice(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_temperature_boundaries_and_independent_rain_advice(self):
        cases = [
            (4, "no", ["Wear a coat."]),
            (4, " YES ", ["Wear a coat.", "Take an umbrella."]),
            (5, "no", ["Wear a jacket."]),
            (17, " YES ", ["Wear a jacket.", "Take an umbrella."]),
            (18, "yes", ["A light layer is enough.", "Take an umbrella."]),
            (25, "No", ["A light layer is enough."]),
        ]
        for temperature, rain_answer, expected_lines in cases:
            with self.subTest(temperature=temperature, rain_answer=rain_answer):
                result = run_script(self.script_path(), input=f'{temperature}\n{rain_answer}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                self.assertEqual(
                    result.stdout.strip().splitlines(),
                    expected_lines,
                    f"For temperature {temperature} and rain answer "
                    f"{rain_answer!r}, print the matching temperature advice first "
                    "and the independent umbrella advice when applicable.",
                )


if __name__ == "__main__":
    unittest.main()

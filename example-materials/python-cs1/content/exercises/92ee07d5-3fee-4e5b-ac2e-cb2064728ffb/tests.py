# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "main.py")


class TestParcelDeliveryQuote(unittest.TestCase):
    def assert_quote(self, entered_lines, expected_lines):
        result = run_script(SCRIPT_PATH, input='\n'.join(entered_lines) + '\n')

        self.assertEqual(
            result.returncode,
            0,
            f"The program must run successfully. Python reported:\n{result.stderr}",
        )
        actual_lines = result.stdout.strip().splitlines()
        self.assertEqual(
            len(actual_lines),
            6,
            "Print exactly the six specified quote lines and no additional output.",
        )
        field_names = [
            "name",
            "destination",
            "weight class",
            "base price",
            "delivery type",
            "total price",
        ]
        for field_name, actual, expected in zip(
            field_names, actual_lines, expected_lines
        ):
            self.assertEqual(
                actual,
                expected,
                f"The {field_name} line is incorrect. Check that field's "
                "calculation, normalization, wording, and required formatting.",
            )

    def test_light_local_standard_delivery(self):
        self.assert_quote(
            ["Ada", "local", "1.9", "no"],
            [
                "Name: Ada",
                "Destination: local",
                "Weight class: light",
                "Base price: 4.75 euros",
                "Delivery: standard",
                "Total price: 4.75 euros",
            ],
        )

    def test_two_kilograms_is_standard(self):
        self.assert_quote(
            ["Ben", "national", "2", "no"],
            [
                "Name: Ben",
                "Destination: national",
                "Weight class: standard",
                "Base price: 5.00 euros",
                "Delivery: standard",
                "Total price: 9.00 euros",
            ],
        )

    def test_ten_kilograms_is_standard_and_inputs_are_normalized(self):
        self.assert_quote(
            ["  Chen  ", "  INTERNATIONAL  ", "10", "  YES  "],
            [
                "Name: Chen",
                "Destination: international",
                "Weight class: standard",
                "Base price: 25.00 euros",
                "Delivery: express",
                "Total price: 43.00 euros",
            ],
        )

    def test_weight_above_ten_is_heavy(self):
        self.assert_quote(
            ["Devi", "national", "10.1", "no"],
            [
                "Name: Devi",
                "Destination: national",
                "Weight class: heavy",
                "Base price: 25.25 euros",
                "Delivery: standard",
                "Total price: 29.25 euros",
            ],
        )

    def test_express_surcharge_is_independent(self):
        self.assert_quote(
            ["Eli", "local", "3.5", "yes"],
            [
                "Name: Eli",
                "Destination: local",
                "Weight class: standard",
                "Base price: 8.75 euros",
                "Delivery: express",
                "Total price: 14.75 euros",
            ],
        )

    def test_national_express_combines_both_surcharges(self):
        self.assert_quote(
            ["Faye", "national", "3", "yes"],
            [
                "Name: Faye",
                "Destination: national",
                "Weight class: standard",
                "Base price: 7.50 euros",
                "Delivery: express",
                "Total price: 17.50 euros",
            ],
        )


if __name__ == "__main__":
    unittest.main()

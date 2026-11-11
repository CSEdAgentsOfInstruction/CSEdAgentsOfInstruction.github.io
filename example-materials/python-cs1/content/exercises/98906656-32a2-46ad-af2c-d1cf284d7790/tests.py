# Adapted for browser execution; assertions retain the original exercise contract.
from workshop_support import run_script
import os
import sys
import unittest


class TestPriceWithTax(unittest.TestCase):
    def script_path(self):
        return os.path.join(os.path.dirname(__file__), "main.py")

    def test_adds_twenty_five_point_five_percent_vat(self):
        for price in [10.50, 0.0, 12.30, 99.99]:
            with self.subTest(price=price):
                result = run_script(self.script_path(), input=f'{price}\n')
                self.assertEqual(
                    result.returncode,
                    0,
                    f"The program must run successfully. Python reported:\n{result.stderr}",
                )
                try:
                    actual = float(result.stdout.strip())
                except ValueError:
                    self.fail("Print only the numeric final price.")
                self.assertAlmostEqual(
                    actual,
                    price * 1.255,
                    places=7,
                    msg="The final price must contain the original price plus 25.5% VAT.",
                )


if __name__ == "__main__":
    unittest.main()

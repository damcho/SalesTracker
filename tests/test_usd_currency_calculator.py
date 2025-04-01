import unittest
from usd_conversions_app.usd_currency_calculator import CurrencyConversion, USDCurrencyCalculator

class test_usd_currency_calculator(unittest.TestCase):

    def test_adds_usd_currenciy_conversions_to_initial_currencies(self):
        initial_currencies = [
            CurrencyConversion(from_currency="EUR", to_currency="USD", rate=1.18),
            CurrencyConversion(from_currency="GBP", to_currency="EUR", rate=1.12),
            CurrencyConversion(from_currency="CAD", to_currency="JPY", rate=80),
            CurrencyConversion(from_currency="BRL", to_currency="CAD", rate=0.19),
            CurrencyConversion(from_currency="JPY", to_currency="GBP", rate=0.007),
            CurrencyConversion(from_currency="AUD", to_currency="ZAR", rate=10.0),
            CurrencyConversion(from_currency="ZAR", to_currency="INR", rate=5),
            CurrencyConversion(from_currency="USD", to_currency="INR", rate=83.96)
        ]
        
        expected_added_currencies = {
            CurrencyConversion(from_currency="EUR", to_currency="USD", rate=1.18),
            CurrencyConversion(from_currency="GBP", to_currency="EUR", rate=1.12),
            CurrencyConversion(from_currency="CAD", to_currency="JPY", rate=80),
            CurrencyConversion(from_currency="BRL", to_currency="CAD", rate=0.19),
            CurrencyConversion(from_currency="JPY", to_currency="GBP", rate=0.007),
            CurrencyConversion(from_currency="AUD", to_currency="ZAR", rate=10.0),
            CurrencyConversion(from_currency="ZAR", to_currency="INR", rate=5),
            CurrencyConversion(from_currency="USD", to_currency="INR", rate=83.96),
            CurrencyConversion(from_currency="INR", to_currency="USD", rate=0.011910433539780848),
            CurrencyConversion(from_currency="GBP", to_currency="USD", rate=1.3216),
            CurrencyConversion(from_currency="CAD", to_currency="USD", rate=0.7400960000000001),
            CurrencyConversion(from_currency="BRL", to_currency="USD", rate=0.14061824),
            CurrencyConversion(from_currency="ZAR", to_currency="USD", rate=0.05955216769890424),
            CurrencyConversion(from_currency="AUD", to_currency="USD", rate=0.5955216769890425),
            CurrencyConversion(from_currency="JPY", to_currency="USD", rate=0.009251200000000001)
        }
        
        added_currencies = USDCurrencyCalculator.currencies_to_usd(initial_currencies)
        
        # Test if the counts are equal
        self.assertEqual(len(added_currencies), len(expected_added_currencies))
        
        # Test if the sets are equal
        self.assertEqual(set(added_currencies), expected_added_currencies)

if __name__ == "__main__":
    unittest.main()

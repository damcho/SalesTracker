from typing import List
from usd_conversions_app.currency_conversion import CurrencyConversion, CurrencyConversionError

class CurrencyNode:
    def __init__(self, currency_conversion: CurrencyConversion):
        self.currency_conversion = currency_conversion
        self.next_currency_nodes: List['CurrencyNode'] = []

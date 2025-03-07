class CurrencyConversion:
    def __init__(self, from_currency: str, to_currency: str, rate: float):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate

    def __eq__(self, other):
        if isinstance(other, CurrencyConversion):
            return (self.from_currency == other.from_currency and
                    self.to_currency == other.to_currency and
                    self.rate == other.rate)
        return False

    def __hash__(self):
        return hash((self.from_currency, self.to_currency, self.rate))


class CurrencyConversionError(Exception):
    pass

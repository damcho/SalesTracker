from typing import List, Set

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


class CurrencyTransformer:
    
    @staticmethod
    def add_currency_conversions(for_currency: str, to_currencies: List[CurrencyConversion]) -> Set[CurrencyConversion]:
        currencies_set = set(to_currencies)
        for a_currency in to_currencies:
            if a_currency.from_currency == for_currency:
                inverted_conversion = CurrencyConversion(
                    from_currency=a_currency.to_currency,
                    to_currency=a_currency.from_currency,
                    rate=1 / a_currency.rate
                )
                currencies_set.add(inverted_conversion)
        return currencies_set
    
    @staticmethod
    def currencies_to_usd(currencies: List[CurrencyConversion]) -> List[CurrencyConversion]:
        currencies_plus_inverted_usd_conversions = list(
            CurrencyTransformer.add_currency_conversions(for_currency="USD", to_currencies=currencies)
        )
        currencies_plus_usd_conversions = currencies_plus_inverted_usd_conversions.copy()

        missing_usd_currency_conversions = [
            currency for currency in currencies if currency.to_currency != "USD" and currency.from_currency != "USD"
        ]

        for missing_usd_conversion in missing_usd_currency_conversions:
            rate = CurrencyTransformer.usd_conversion_rate(
                missing_usd_conversion, currencies_plus_inverted_usd_conversions
            )
            currencies_plus_usd_conversions.append(
                CurrencyConversion(
                    from_currency=missing_usd_conversion.from_currency,
                    to_currency="USD",
                    rate=rate
                )
            )

        return currencies_plus_usd_conversions

    @staticmethod
    def usd_conversion_rate(new_currency: CurrencyConversion, currency_conversions: List[CurrencyConversion]) -> float:
        for currency_conversion in currency_conversions:
            if currency_conversion.from_currency == new_currency.to_currency and currency_conversion.to_currency == "USD":
                return currency_conversion.rate
        
        filtered_conversions = [
            conversion for conversion in currency_conversions if conversion.from_currency == new_currency.to_currency
        ]
        
        for a_conversion in filtered_conversions:
            try:
                return new_currency.rate * CurrencyTransformer.usd_conversion_rate(a_conversion, currency_conversions)
            except CurrencyConversionError:
                continue
        
        raise CurrencyConversionError(f"Unable to convert {new_currency.from_currency} to USD.")



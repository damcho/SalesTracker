from typing import List, Set
from usd_conversions_app.currency_conversion import CurrencyConversion, CurrencyConversionError
from usd_conversions_app.currency_node import CurrencyNode

class USDCurrencyCalculator:

    @staticmethod
    def make_currency_conversions_nodes_graph(currency_conversions: List[CurrencyConversion]) -> List[CurrencyNode]:
        currency_nodes = [CurrencyNode(currency_conversion) for currency_conversion in currency_conversions]
        
        for node in currency_nodes:
            next_nodes = [a_currency_node for a_currency_node in currency_nodes
                          if node.currency_conversion.to_currency == a_currency_node.currency_conversion.from_currency]
            node.next_currency_nodes.extend(next_nodes)
        
        return currency_nodes

    @staticmethod
    def calculate_rate(currency: str, from_currency_node: CurrencyNode) -> float:
        if from_currency_node.currency_conversion.to_currency == "USD":
            return from_currency_node.currency_conversion.rate

        for next_currency_node in from_currency_node.next_currency_nodes:
            try:
                return from_currency_node.currency_conversion.rate * USDCurrencyCalculator.calculate_rate(currency, next_currency_node)
            except CurrencyConversionError:
                continue
        
        raise CurrencyConversionError(f"Unable to convert {currency} to USD")

    @staticmethod
    def usd_conversion(currency: str, currency_nodes: List[CurrencyNode]) -> CurrencyConversion:
        starting_nodes = [node for node in currency_nodes if node.currency_conversion.from_currency == currency]

        for currency_node in starting_nodes:
            try:
                return CurrencyConversion(
                    from_currency=currency,
                    to_currency="USD",
                    rate=USDCurrencyCalculator.calculate_rate(currency, currency_node)
                )
            except CurrencyConversionError:
                continue
        
        raise CurrencyConversionError(f"Unable to convert {currency} to USD")

    @staticmethod
    def add_currency_conversions(currency: str, currencies: List[CurrencyConversion]) -> Set[CurrencyConversion]:
        currencies_set = set(currencies)
        for a_currency in currencies:
            if a_currency.from_currency == currency:
                currencies_set.add(
                    CurrencyConversion(from_currency=a_currency.to_currency, to_currency=a_currency.from_currency, rate=1 / a_currency.rate)
                )
        return currencies_set

    @staticmethod
    def get_missing_currency_conversions_to_usd(currencies: List[CurrencyConversion]) -> List[str]:
        return [currency_conversion.from_currency for currency_conversion in currencies
                if currency_conversion.to_currency != "USD" and currency_conversion.from_currency != "USD"]

    @staticmethod
    def currencies_to_usd(currencies: List[CurrencyConversion]) -> List[CurrencyConversion]:
        currencies_plus_inverted_usd_conversions = list(USDCurrencyCalculator.add_currency_conversions("USD", currencies))
        currencies_plus_usd_conversions = currencies_plus_inverted_usd_conversions

        missing_usd_currency_conversions = USDCurrencyCalculator.get_missing_currency_conversions_to_usd(currencies_plus_usd_conversions)

        currency_graph = USDCurrencyCalculator.make_currency_conversions_nodes_graph(currencies_plus_inverted_usd_conversions)

        for missing_currency_conversion in missing_usd_currency_conversions:
            currencies_plus_usd_conversions.append(
                USDCurrencyCalculator.usd_conversion(missing_currency_conversion, currency_graph)
            )

        return currencies_plus_usd_conversions

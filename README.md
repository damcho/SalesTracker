# Currency conversions Middleware API

## Description
### Middleware API which loads an array of currency conversion rates and calculates and adds the missing currency conversions to USD and returns the initial currencies plus the calculated ones to the client

## Tech stack
- Python 3
- Flask
- requests
- Flask-JSON
- gunicorn

## USD Currency Calculator
In order to calculate the missing USD conversions the USD currency calculator does the following steps
- from the original conversion rates, it checks if any of the currency conversions has `USD` as the convertible currency, and inverts it by making a `USD` convertible currency.
For example if we have 

```
CurrencyConversion(from: "USD", to: "EUR", rate: 1.2)
```
then the algorithm adds
```
CurrencyConversion(from: "EUR", to: "USD", rate: 1 / 1.2)
```

- Filter the currencies that already have a `USD` conversion
- From the filtered currencies it iterates on each one by checking if the `to_currency` field of the rest of the currencies is `USD` in which case it returns the conversion rate. Otherwise, it calls recursively with another currency that has the `to_currency` field equal to the `from_curency` of the previous currency conversion object. So for esample
if we had 
```
[
    (from_currency: "ARS", to_currency: "EUR"),
    (from_currency: "EUR", to_currency: "GBP"),
    (from_currency: "GBP", to_currency: "USD")
]
```
then the algorithm would grab the missing USD conversion `(from_currency: "ARS", to_currency: "EUR")` and then check recursively over the currencies that connect the original one through the `to_currency` field until it finds that there is a currency `to_currency` field that is equal to `USD` and multiply the rate with the previous conversion rates.



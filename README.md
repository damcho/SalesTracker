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

### Adds inverted Currency Conversions

- from the original conversion rates, it checks if any of the currency conversions has `USD` as the convertible currency, and inverts it by making a `USD` convertible currency.
For example if we have 

```
CurrencyConversion(from: "USD", to: "EUR", rate: 1.2)
```
then the algorithm adds
```
CurrencyConversion(from: "EUR", to: "USD", rate: 1 / 1.2)
```

### Creates Currency conversions Graph

- Creates a one way graph of Linked Nodes where each node contains a currency conversion and a reference to an array of other nodes where the `to_currency` field of the current node, matches the `from_currency` field of the linked nodes

### Create missing currency conversions

- Filter the currencies that already have a `USD` conversion
- From the filtered currencies it iterates on each one and calculates the USD currency conversion by finding the `starting nodes` (nodes that contain the `from_currency` field for the currency we want to create a conversion) And follows the node's linked connections until it finds a destination with a USD conversion. If there isn't one, it throws an error and starts over from another starting node.

## Known Issues
The original currencies data source should not create a graph that contains cycles since this could create an infinite loop when building a USD conversion

for example 
```
EUR -> ARS -----> ARS -> JPY ------> JPY -> EUR
```
Is an invalid graph configuration.

```
EUR -> ARS -----> ARS -> JPY ------> JPY -> USD
```

Is a valid graph configuration

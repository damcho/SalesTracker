from flask import Flask, request, jsonify
import requests
from CurrencyConversion import CurrencyConversion
from CurrencyTransformer import CurrencyTransformer

app = Flask(__name__)

# Middleware to process GET requests
@app.before_request
def before_request():
    # Check if it's a GET request to the specific endpoint
    if request.method == 'GET' and request.endpoint == 'rates':
        # Perform an external GET request to another service
        response = requests.get('https://ile-b2p4.essentialdeveloper.com/rates')
        
        # If the response is successful (status code 200)
        if response.status_code == 200:
            # Transform the response (e.g., adding a custom key-value pair)
            data = response.json()

            currencyConversionsArray = [CurrencyConversion(currencyconversion['from'], currencyconversion['to'], currencyconversion['rate']) for currencyconversion in data]
            addedCurrencies = CurrencyTransformer.currencies_to_usd(currencies=currencyConversionsArray)
            # Add the transformed data to the request context (you can also modify the response directly here)
            currencies_conversions_json_list = [added_currency_conversion.to_dict() for added_currency_conversion in addedCurrencies]

            request.transformed_data = currencies_conversions_json_list
        else:
            request.transformed_data = {"error": "External request failed"}

# Route to handle the transformed data
@app.route('/rates', methods=['GET'])
def rates():
    # Return the transformed data (or error if the external request failed)
    return jsonify(request.transformed_data)

if __name__ == '__main__':
    app.run(debug=True)

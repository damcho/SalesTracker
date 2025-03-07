from flask import Flask, request, jsonify
import requests
from CurrencyConversion import CurrencyConversion
from CurrencyTransformer import CurrencyTransformer

app = Flask(__name__)

@app.before_request
def before_request():
    if request.method == 'GET' and request.endpoint == 'rates':
        response = requests.get('https://ile-b2p4.essentialdeveloper.com/rates')
        
        if response.status_code == 200:
            data = response.json()

            currencyConversionsArray = [CurrencyConversion(currencyconversion['from'], currencyconversion['to'], currencyconversion['rate']) for currencyconversion in data]
            addedCurrencies = CurrencyTransformer.currencies_to_usd(currencies=currencyConversionsArray)
            currencies_conversions_json_list = [added_currency_conversion.to_dict() for added_currency_conversion in addedCurrencies]

            request.transformed_data = currencies_conversions_json_list
        else:
            request.transformed_data = {"error": "External request failed"}

@app.route('/rates', methods=['GET'])
def rates():
    return jsonify(request.transformed_data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import requests
from usd_conversions_app.currency_conversion import CurrencyConversion
from usd_conversions_app.usd_currency_calculator import USDCurrencyCalculator

app = Flask(__name__)

@app.before_request
def before_request():
    if request.method == 'GET' and request.endpoint == 'rates':
        ed_rates_response = requests.get('https://ile-b2p4.essentialdeveloper.com/rates')
        
        if ed_rates_response.status_code == 200:
            ed_rates = ed_rates_response.json()

            currencyConversionsArray = [
                CurrencyConversion(
                  currencyconversion['from'], 
                  currencyconversion['to'],
                  currencyconversion['rate']
                ) for currencyconversion in ed_rates
            ]

            ed_rates_plus_added_usd_conversions = USDCurrencyCalculator.currencies_to_usd(
                currencies=currencyConversionsArray
            )
            currencies_conversions_json_list = [
                added_usd_currency_conversion.to_dict() 
                for added_usd_currency_conversion in ed_rates_plus_added_usd_conversions
            ]

            request.transformed_data = currencies_conversions_json_list
        else:
            request.transformed_data = {"error": "External request failed"}

@app.route('/rates', methods=['GET'])
def rates():
    return jsonify(request.transformed_data)

if __name__ == '__main__':
    app.run(debug=True)

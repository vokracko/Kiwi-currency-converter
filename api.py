#!/usr/bin/env python3
import json
import logging

from flask import Flask, request, make_response, jsonify
from currency_converter import CurrencyConverter, CurrencyError

app = Flask(__name__)


@app.route('/currency_converter', methods=['GET'])
def currency_converter():
    """Handle requests for converting currencies."""
    amount = request.args.get("amount")
    input_currency = request.args.get("input_currency")
    output_currency = request.args.get("output_currency")

    if amount is None or input_currency is None:
        return make_response(jsonify({
            "error": "Missing required value(s)",
            "description": "amount or input_currency is not specified"}), 400)

    if not amount or not input_currency:
        return make_response(jsonify({
            "error": "Value(s) not specified",
            "description": "amount or input_currency has no value"}), 400)

    try:
        converter.load_rates()
        result = converter.convert(input_currency,
                                   output_currency,
                                   float(amount))
    except CurrencyError:
        # json.dumps converts utf8 codes into symbols, jsonify couldn't
        return make_response(json.dumps({
            "error": "Invalid currency",
            "supportedCurrencies": converter.codes}, ensure_ascii=False), 400)
    except Exception as e:
        logging.exception(e)
        return make_response(jsonify({"error": "Server error"}), 500)

    return make_response(jsonify(result), 200)


@app.errorhandler(404)
def error_handler(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    converter = CurrencyConverter()
    app.run()

#!/usr/bin/env python3

import json
import argparse
import requests


class CurrencyConverter:
    API_KEY = "b3bcc9bd8327488f921e006b3d4b7765"
    API_URL = "https://openexchangerates.org/api/latest.json"

    rates = {}
    codes = {}

    def __init__(self):
        """Load currency codes and rates."""
        self.load_codes()
        self.load_rates()

    def convert(self, input_currency, output_currency, amount):
        """Convert between currencies.

        Convert given amount of input_currency to output_currency,
        or all available currencies if output_currency is None

        :param str input_currency: Currency code or symbol
        :param str output_currency: Currency code, symbol or None
        :param float amount
        :return: Result of conversion including input informations
        :rtype: dict
        """
        input_currency = self.symbol2code(input_currency)
        usd = amount / self.rates[input_currency]
        result = {
            "input": {"amount": amount, "currency": input_currency},
            "output": {}
        }

        if output_currency is None:
            for key, value in self.rates.items():
                if key == output_currency:
                    continue

                result["output"][key] = usd * value

        else:
            output_currency = self.symbol2code(output_currency)
            result["output"][output_currency] = usd * self.rates[output_currency]

        return result

    def symbol2code(self, symbol):
        """Convert currency symbol to its code."""
        code = self.codes.get(symbol)

        if code is None:
            code = symbol

        if code not in self.rates:
            raise CurrencyError("Invalid currency")

        return code

    def load_codes(self):
        """Load currency codes and symbols."""
        with open("codes.json") as fd:
            self.codes = json.load(fd)

    def load_rates(self):
        """Load currency rates with base USD."""
        response = requests.get(self.API_URL, params={"app_id": self.API_KEY})

        if response.status_code != 200:
            raise Exception("Failed to get currency rates")
        self.rates = response.json()["rates"]


class CurrencyError(Exception):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument("--amount", type=float, required=True)
    required.add_argument("--input_currency", required=True)
    parser.add_argument("--output_currency", default=None)
    args = parser.parse_args()

    converter = CurrencyConverter()
    result = converter.convert(args.input_currency,
                               args.output_currency,
                               args.amount)

    print(json.dumps(result, indent=4))

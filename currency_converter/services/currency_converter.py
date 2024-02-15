import json
from decimal import Decimal

import requests

from currency_converter.models import CurrencyConversion


class ConversionFileService:
    @staticmethod
    def load_from_file(from_currency, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return [CurrencyConversion(
            from_currency=from_currency,
            to_currency=conversion['code'],
            rate=conversion['rate'],
            name=conversion['name']
        ) for conversion in data.values()]

    @staticmethod
    def load_from_url(from_currency, url):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            direct_list = [CurrencyConversion(
                from_currency=from_currency,
                to_currency=conversion['code'],
                rate=conversion['rate'],
                name=conversion['name']
            ) for conversion in data.values()]
            inverse_list = [CurrencyConversion(
                from_currency=conversion['code'],
                to_currency=from_currency,
                rate=conversion['inverseRate'],
                name=conversion['name']
            ) for conversion in data.values()]
            return direct_list + inverse_list
        else:
            raise ValueError("Failed to fetch data from URL")


class CurrencyConversionService:

    def convert(self, from_currency, to_currency, amount):
        amount = Decimal(str(amount))
        conversion = CurrencyConversion.objects.filter(
            from_currency=from_currency
        ).filter(to_currency=to_currency).first()
        if not conversion:
            raise ValueError("Conversion not available")
        return amount * conversion.rate



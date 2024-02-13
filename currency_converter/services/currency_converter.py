import json
import requests


class CurrencyConversion:
    def __init__(self, from_currency, to_currency, rate, name):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate
        self.name = name

    def __lt__(self, other):
        return self.rate < other.rate

    def __eq__(self, other):
        return self.rate == other.rate


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
    def __init__(self, conversion_data):
        self.conversion_data = conversion_data

    def convert(self, from_currency, to_currency, amount):
        conversion = self._find_conversion(from_currency, to_currency)
        if not conversion:
            raise ValueError("Conversion not available")
        return amount * conversion.rate

    def get_rate_for(self, from_currency, to_currency):
        conversion = self._find_conversion(from_currency, to_currency)
        if not conversion:
            raise ValueError("Conversion not available")
        return conversion.rate

    def _find_conversion(self, from_currency, to_currency):
        for conversion in self.conversion_data:
            if conversion.from_currency == from_currency and conversion.to_currency == to_currency:
                return conversion
        return None


if __name__ == "__main__":
    conversion_data = ConversionFileService.load_from_url('MDL', 'https://www.floatrates.com/daily/mdl.json')

    converter = CurrencyConversionService(conversion_data)

    amount_in_eur = converter.convert("MDL", "EUR", 2000)
    print(f"Amount in EUR: {amount_in_eur:.2f}")
    amount_in_mdl = converter.convert("EUR", "MDL", 2000)
    print(f"Amount in MDL: {amount_in_mdl:.2f}")

    rate_eur = converter.get_rate_for("MDL", "EUR")
    print(f"Rate from MDL to EUR: {rate_eur}")

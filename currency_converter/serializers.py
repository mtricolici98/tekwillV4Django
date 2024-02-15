from rest_framework import serializers

from currency_converter.models import ConversionHistory, CurrencyConversion


class ConversionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistory
        fields = ['currency', 'amount', 'timestamp']


class CurrencyConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConversion
        fields = ['from_currency', 'to_currency', 'rate']

from rest_framework import serializers

from currency_converter.models import ConversionHistory


class ConversionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistory
        fields = ['currency', 'amount', 'timestamp']

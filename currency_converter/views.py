from rest_framework.decorators import api_view
from rest_framework.response import Response

from currency_converter.models import ConversionHistory, CurrencyConversion
from currency_converter.serializers import ConversionHistorySerializer, CurrencyConversionSerializer
from currency_converter.services.currency_converter import ConversionFileService, CurrencyConversionService


# Create your views here.

@api_view(['GET'])
def hello_world(request):
    for header, value in request.headers.items():
        print(header, value)
    return Response("<h1>Hello World!</h1>")


@api_view(['GET'])
def convert(request, currency, amount):
    try:
        amount = float(amount)
    except ValueError:
        return Response({"error": "Invalid amount"}, status=400)
    converter = CurrencyConversionService()
    try:
        amount_in_eur = converter.convert("MDL", currency, amount)
        ConversionHistory.objects.create(
            amount=amount,
            currency=currency
        )
    except ValueError:
        return Response({"error": "Invalid"}, status=400)
    return Response({'result': amount_in_eur})


@api_view(['POST'])
def convert_post(request):
    currency = request.data['currency']
    try:
        amount = float(request.data['amount'])
    except ValueError:
        return Response({"error": "Invalid amount"}, status=400)
    converter = CurrencyConversionService()
    try:
        amount_in_eur = converter.convert("MDL", currency, amount)
        ConversionHistory.objects.create(
            amount=amount,
            currency=currency
        )
    except ValueError:
        return Response({"error": "Invalid"}, status=400)
    return Response({'result': amount_in_eur})


@api_view(['GET'])
def conversion_history(request):
    currency = request.query_params.get('currency', None)
    if currency:
        conversion_elements = ConversionHistory.objects.filter(currency=currency)
    else:
        conversion_elements = ConversionHistory.objects.all()
    response_data = ConversionHistorySerializer(conversion_elements, many=True).data
    return Response({'result': response_data, 'currency': currency})


@api_view(['POST'])
def load_conversion(request):
    conversion_object = ConversionFileService.load_from_url(
        'MDL',
        'https://www.floatrates.com/daily/mdl.json'
    )
    for conversion in conversion_object:
        # Caut daca deja exista
        if CurrencyConversion.objects.filter(from_currency=conversion.from_currency,
                                             to_currency=conversion.to_currency).exists():
            # Get the object that exists from the database
            existing_conversion = CurrencyConversion.objects.filter(
                from_currency=conversion.from_currency,
                to_currency=conversion.to_currency).first()
            existing_conversion.rate = conversion.rate
            existing_conversion.save()
        else:
            conversion.save(force_insert=True)
    return Response(status=200)


@api_view(['GET'])
def get_all_conversions_available(request):
    all_cc = CurrencyConversion.objects.all()
    serialized = CurrencyConversionSerializer(all_cc, many=True).data
    return Response(data=serialized, status=200)

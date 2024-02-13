from rest_framework.decorators import api_view
from rest_framework.response import Response

from currency_converter.models import ConversionHistory
from currency_converter.serializers import ConversionHistorySerializer
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
    conversion_data = ConversionFileService.load_from_url('MDL', 'https://www.floatrates.com/daily/mdl.json')
    converter = CurrencyConversionService(conversion_data)
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
    conversion_data = ConversionFileService.load_from_url('MDL', 'https://www.floatrates.com/daily/mdl.json')
    converter = CurrencyConversionService(conversion_data)
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

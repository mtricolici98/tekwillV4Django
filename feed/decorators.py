import functools
from datetime import datetime

from django.utils import timezone
from rest_framework.response import Response

from feed.models import Token


def login_decorator(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response(status=401)
        token = request.headers['Authorization']
        token_object = Token.objects.filter(token=token).first()
        if not token_object:
            return Response(status=401)
        if token_object.expires_on < timezone.now():
            token_object.delete()
            return Response(status=401)
        request.user = token_object.user
        return view_func(request, *args, **kwargs)

    return wrapper


from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response


def request_get_or_none(request, key):
    value = request.data.get(key, None)
    if value is None:
        return None
    else:
        return value


def request_get_query_or_none(request, key):
    value = request.GET.get(key, None)
    if value is None:
        return None
    else:
        return value

def request_get_query_or_raise_error(request, field, message=None):
    value = request.GET.get(field, None)
    if value is None:
        if message is None:
            raise serializers.ValidationError({field: "This query is required."})
        else:
            raise serializers.ValidationError({field: message})
    else:
        return value

def request_get_or_raise_error(request, field, message=None):
    value = request.data.get(field, None)
    if value is None:
        if message is None:
            raise serializers.ValidationError({field: "This field is required."})
        else:
            raise serializers.ValidationError({field: message})
    else:
        return value


def raise_required_key(key):
    return Response(
        status=status.HTTP_400_BAD_REQUEST, data={key: "this key is required."}
    )

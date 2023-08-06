from rest_framework import serializers

def dict_get_or_raise_error(dict_, key, message=None):
    value = dict_.get(key, None)
    if value is None:
        if message is None:
            raise serializers.ValidationError({key: "This field is required."})
        else:
            raise serializers.ValidationError({key: message})
    else:
        return value
        
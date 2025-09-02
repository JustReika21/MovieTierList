from django.core.exceptions import ValidationError


def validate_description_length(value):
    if len(value) > 2048:
        raise ValidationError('Description must be shorter than 1024 symbols')

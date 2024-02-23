from django.core.exceptions import ValidationError


def validate_isalpha(value):
    if not value.isalpha():
        raise ValidationError("Name must be only letters.")
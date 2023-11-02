import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.svg']
    if not extension.lower() in valid_extensions:
        raise ValidationError('The field must be a svg file.')

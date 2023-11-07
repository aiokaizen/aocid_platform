import os

from django.utils import timezone
from django.utils.text import slugify


def get_ip_address(request):
    try:
        # ip addresses: 'client,proxy1,proxy2'
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ''
    return ip


def get_model_file_filename(instance, filename):
    filename, ext = os.path.splitext(filename)
    model_name = instance.__class__.__name__.lower()
    now = timezone.now()
    year, month, day = now.year, now.month, now.day
    return f"{year}/{month}/{day}/{model_name}/{slugify(filename)}{ext}"

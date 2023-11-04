import os

from django.utils import timezone
from django.utils.text import slugify


def current_year():
    return timezone.now().year


def get_model_file_filename(instance, filename):
    filename, ext = os.path.splitext(filename)
    print("dir instance:", dir(instance))
    model_name = instance.__class__.__name__.lower()
    now = timezone.now()
    year, month, day = now.year, now.month, now.day
    return f"{year}/{month}/{day}/{model_name}/{slugify(filename)}{ext}"


def get_person_photo_filename(instance, filename):
    _filename, ext = os.path.splitext(filename)
    full_name = slugify(instance.full_name).replace('-', '_')
    return f"person/{full_name}{ext}"


def get_club_logo_filename(instance, filename):
    _filename, ext = os.path.splitext(filename)
    full_name = slugify(instance.name).replace('-', '_')
    return f"club/{full_name}{ext}"


def get_book_file_filename(instance, filename):
    filename, ext = os.path.splitext(filename)
    now = timezone.now()
    year, month, day = now.year, now.month, now.day
    return f"{year}/{month}/{day}/book/{slugify(filename)}{ext}"

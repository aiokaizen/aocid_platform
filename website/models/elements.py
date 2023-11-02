import logging
from datetime import datetime

from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from image_cropping import ImageRatioField
from easy_thumbnails.fields import ThumbnailerImageField
from autoslug import AutoSlugField

from website.validators import validate_file_extension


class Slide(models.Model):
    alignments = [
        ("left", "Left"),
        ("center", "Center"),
        ("right", "Right"),
    ]

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

    title = models.CharField(_("Title"), max_length=255)
    image = ThumbnailerImageField(_("Image"), upload_to="website/sliders/images/")
    description = models.TextField(_("Description"), null=True, blank=True)
    alignment = models.CharField(
        _("Alignment"),
        max_length=255,
        choices=alignments,
        null=True,
        blank=True,
        default="center",
    )

    def __str__(self):
        return f"{self.title} Slide"


class Button(models.Model):
    types = [
        ("video", "video"),
        ("internal link", "internal link"),
        ("external link", "external link"),
    ]

    class Meta:
        verbose_name = _("Button")
        verbose_name_plural = _("Buttons")

    title = models.CharField(_("Title"), max_length=255)
    action = models.URLField(_("URL"))
    type = models.CharField(_("Type"), max_length=255, choices=types)
    slide = models.ForeignKey(Slide, related_name="buttons", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} Button"


class Counter(models.Model):
    class Meta:
        verbose_name = _("Counter")
        verbose_name_plural = _("Counters")

    title = models.CharField(_("Title"), max_length=255)
    icon = models.FileField(
        _("Icon"), upload_to="website/counters/icons",
        validators=[validate_file_extension]
    )
    count_to = models.IntegerField(_("Count To"), default=0)

    def __str__(self):
        return f"{self.title} Counter"

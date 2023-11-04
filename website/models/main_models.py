import logging
from datetime import datetime

from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from image_cropping import ImageRatioField
from easy_thumbnails.fields import ThumbnailerImageField
from autoslug import AutoSlugField

from website.validators import validate_file_extension


class Message(models.Model):

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    name = models.CharField(_("Full name"), max_length=255, default="")
    email = models.EmailField(_("Email"), default="")
    message = models.TextField(_("Message"), default="")
    sent_by_mail = models.BooleanField(_("Sent by mail"), default=False)
    sent_date = models.DateTimeField(_("Sent date"), auto_now_add=True)

    def __str__(self):
        return f"{self.name} Message"

    def create(self):
        self.save()
        self.send_email()

    def send_email(self):
        body = f"\nFrom: {self.name} - {self.email} \nMessage: {self.message}"
        platform_name = getattr(settings, "PLATFORM_NAME", "Ait Ourir Chess Club")
        try:
            send_mail(
                subject=f"New contact message at {platform_name}",
                message=body,
                from_email="noreply@ekblocks.com",
                recipient_list=getattr(settings, "EMAIL_RECIPIENTS", [
                    "mouadkommir@gmail.com"
                ]),
                fail_silently=False,
            )
            self.sent_by_mail = True
            self.save(update_fields=["sent_by_mail"])
        except Exception as e:
            logger = logging.getLogger("errors")
            logger.error("ERROR : {:s}".format(e))


class NewsLetter(models.Model):
    """ Get emails from people that want to subscribe to one of our newsletter. """

    class Meta:
        verbose_name = _("NewsLetter")
        verbose_name_plural = _("NewsLetters")

    name = models.CharField(_("Nom"), max_length=256)
    slug = AutoSlugField(unique=True)
    emails = models.TextField(
        _("Liste des e-mails"), default="", blank=True,
        help_text=_("Une adresse email par ligne.")
    )
    json_emails = models.JSONField("Emails list", default=list)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name

        if "update_fields" in kwargs and "emails" in kwargs["update_fields"]:
            self.json_emails = self.emails.replace("\r\n", "\n").split("\n")
            kwargs["update_fields"].append("json_emails")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({len(self.json_emails)} emails)"

    def add_email(self, email):
        if not self.json_emails:
            self.json_emails = []

        try:
            validate_email(email)

            self.json_emails.append(email)
            self.emails += f"{email}\n"
            self.save(update_fields=["emails", "json_emails"])
            return {
                "result": "success",
                "message": _("L'adresse email est ajoutée avec succès.")
            }
        except ValidationError as e:
            return {
                "result": "error",
                "error_code": "invalid",
                "message": _("L'adresse email n'est pas valide.")
            }


class Application(models.Model):
    """
    Might be used to get requests from people to join our committee?
    """

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")

    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    birthday = models.DateField(_("Birthday"), blank=True, null=True)
    email = models.EmailField(_("E-mail"))
    cv = models.FileField(_("Cv"), upload_to="website/cv_files/")
    message = models.TextField(_("Message"), blank=True)
    sent_by_mail = models.BooleanField(_("Sent by mail"), default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    def create(self):
        self.save()
        self.send_email()

    def send_email(self):
        body = f"\nFrom: {self.full_name} - {self.email} \nMessage: {self.message}"
        platform_name = getattr(settings, "PLATFORM_NAME", "Ait Ourir Chess Club")
        try:
            send_mail(
                subject=f"New contact message at {platform_name}",
                message=body,
                from_email="noreply@ekblocks.com",
                recipient_list=getattr(settings, "EMAIL_RECIPIENTS", [
                    "mouadkommir@gmail.com"
                ]),
                fail_silently=False,
            )
            self.sent_by_mail = True
            self.save(update_fields=["sent_by_mail"])
        except Exception as e:
            logger = logging.getLogger("errors")
            logger.error("ERROR : {:s}".format(e))


class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        unique_together = ("slug", "content_type")

    def __str__(self):
        return f"{self.name}"

    name = models.CharField(_("Name"), max_length=256)
    slug = AutoSlugField(populate_from="name")
    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return f"{self.content_type or ''} {self.name}"


class Project(models.Model):
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return f"{self.name}"

    name = models.CharField(_("Name"), max_length=256)
    slug = AutoSlugField(populate_from="name", unique=True)
    short_description = models.CharField(_("Short Description"), max_length=256)
    image = ThumbnailerImageField(
        _("Image"),
        upload_to="website/projects/projects_images/",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="projects"
    )
    published_at = models.DateTimeField(_("Published_at"), default=datetime.now)
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True)

    @classmethod
    def get_published_projects(cls):
        return cls.objects.filter(published_at__lte=datetime.now())

    @classmethod
    def get_latest_projects(self, num):
        projects = Project.get_published_projects()
        return projects.order_by("-published_at")[:num]

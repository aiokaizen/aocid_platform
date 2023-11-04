from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from django.utils import timezone

from easy_thumbnails.fields import ThumbnailerImageField
from autoslug import AutoSlugField

from club import settings as club_settings
from club.models.person_models import Player, Member
from club.utils import (
    get_person_photo_filename,
    get_club_logo_filename,
    current_year,
    get_model_file_filename,
    get_book_file_filename
)


class Club(models.Model):

    singleton = True

    class Meta:
        verbose_name = _("Club")
        verbose_name_plural = _("Club")

    name = models.CharField(_("Nom du club"), max_length=256)
    logo = ThumbnailerImageField(
        _("Logo"), upload_to=get_club_logo_filename, blank=True, null=True
    )
    sold = models.DecimalField(
        _("Solde"), max_digits=12, decimal_places=2, default=0, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Implementing Singleton Model
        if not self.id and Club.objects.all().exists():
            # We have already created our club
            raise Exception(_(
                "Le club est déjà créé. Merci de le modifier pour effectuer des changements."
            ))

        return super().save(*args, **kwargs)

    @classmethod
    def get_club(cls):
        return cls.objects.first()


class Insurance(models.Model):

    class Meta:
        verbose_name = _("Assurance")
        verbose_name_plural = _("Assurances")

    year = models.PositiveSmallIntegerField(
        _("Année"), default=current_year
    )
    amount = models.DecimalField(
        _("Montant"), max_digits=8, decimal_places=2,
        help_text=_("Le montant à payer pour l'assurance.")
    )

    def __str__(self):
        return str(_("Assurance de l'année %(year)s" % { "year": self.year}))


class Plan(models.Model):

    class Meta:
        verbose_name = _("Abonnement")
        verbose_name_plural = _("Abonnements")

    name = models.CharField(_("Nom d'abonnement"), max_length=256)
    start_date = models.DateField(_("Date de début"), null=True, blank=True)
    recurring_payment = models.BooleanField(
        _("Paiement récurrent"), default=True,
        help_text=_("Un seule paiement a vie, ou bien un paiement chaque period (mois ou année).")
    )
    period = models.CharField(
        _("Period"), max_length=16, choices=club_settings.PERIOD_CHOICES
    )
    amount = models.DecimalField(_("Montant"), max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.amount} / {self.get_period_display()}"


class Subscription(models.Model):

    class Meta:
        verbose_name = _("Adhésion")
        verbose_name_plural = _("Adhésions")

    date = models.DateField(_("Date d’adhésion"), null=True, blank=True)
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, verbose_name=_("Abonnement")
    )
    player = models.ForeignKey(
        Player, on_delete=models.PROTECT, verbose_name=_("Adhérant")
    )

    def __str__(self):
        return f"{self.player} - {self.plan.name}"


class Book(models.Model):

    class Meta:
        verbose_name = _("Livre")
        verbose_name_plural = _("Livres")

    image = ThumbnailerImageField(_("Image"), upload_to=get_model_file_filename)
    title = models.CharField(_("Titre"), max_length=256)
    book_file = models.FileField(_("Livre"), upload_to=get_book_file_filename)
    category = models.CharField(_("Catégorie"), max_length=64, default="", blank=True)
    author = models.CharField(_("Auteur"), max_length=256, default="", blank=True)
    description = models.TextField(_("Description"), default="", blank=True)
    date = models.DateField(_("Date de sortie"), null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Album(models.Model):

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    title = models.CharField(_("Titre"), max_length=256, unique=True)
    slug = AutoSlugField(populate_from="title", unique=True)
    date = models.DateField(_("Date d'album"), null=True, blank=True)
    description = models.TextField(_("Description"), default="", blank=True)

    def __str__(self):
        return gettext("Album") + " - " + self.title


class Media(models.Model):

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Médiathèque")

    photo = ThumbnailerImageField(_("Photo"), upload_to=get_model_file_filename)
    title = models.CharField(_("Titre"), max_length=256, default="", blank=True)
    date = models.DateField(_("Date de capture"), null=True, blank=True)
    description = models.TextField(_("Description"), default="", blank=True)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title or self.photo.name

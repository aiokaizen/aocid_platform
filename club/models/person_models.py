from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from club import settings as club_settings
from club.utils import (
    get_person_photo_filename,
    get_club_logo_filename
)


class Family(models.Model):

    class Meta:
        verbose_name = _("Famille")
        verbose_name_plural = _("Familles")

    name = models.CharField(_("Nom de la famille"), max_length=256)

    def __str__(self):
        return f"La famille {self.name}"


class Person(models.Model):

    class Meta:
        verbose_name = _("Personne")
        verbose_name_plural = _("Personnes")
        abstract = True

    photo = ThumbnailerImageField(
        _("Photo"), upload_to=get_person_photo_filename, blank=True, null=True
    )
    first_name = models.CharField(_("Prénom"), max_length=256)
    last_name = models.CharField(_("Nom"), max_length=256)
    birthday = models.DateField(_("Date de naissance"), null=True, blank=True)
    birth_place = models.CharField(_("Lieu de naissance"), max_length=256, default="", blank=True)
    cnie = models.CharField(_("CNIE"), max_length=16, default="", blank=True)
    chronic_disease = models.BooleanField(
        _("Souffrez-vous d’une maladie ?"), default=False, blank=True
    )
    disease_description = models.CharField(
        _("Si oui, quelle est la maladie ?"), default="", max_length=256, blank=True
    )

    # Address
    # country = models.CharField(
    #     _("Pays"), max_length=256, default="Maroc", blank=True,
    #     choices=club_settings.COUNTRIES
    # )
    city = models.CharField(
        _("Ville"), max_length=256, default="Ait Ourir", blank=True,
        choices=club_settings.MOROCCAN_CITIES
    )
    postal_code = models.CharField(_("Code postal"), max_length=256, blank=True)
    street_address = models.CharField(_("Adresse"), max_length=256, blank=True)

    # Contact informations
    email = models.EmailField(_("Email"), blank=True)
    phone_number = models.CharField(
        _("Numéro de téléphone"), max_length=32, default="", blank=True
    )
    fix_number = models.CharField(
        _("Numéro de téléphone fixe"), max_length=32, default="", blank=True
    )

    # Social Media
    facebook_account = models.CharField(
        _("Compte Facebook"), max_length=256, default="", blank=True
    )
    instagram_account = models.CharField(
        _("Compte Instagram"), max_length=256, default="", blank=True
    )
    tiktok_account = models.CharField(
        _("Compte TikTok"), max_length=256, default="", blank=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Guardian(Person):

    class Meta:
        verbose_name = _("Tuteur")
        verbose_name_plural = _("Tuteurs")


class Player(Person):

    class Meta:
        verbose_name = _("Personne")
        verbose_name_plural = _("Personnes")

    guardian = models.ForeignKey(
        Guardian, verbose_name=_("Tuteur"), on_delete=models.PROTECT,
        null=True, blank=True
    )

    elo = models.PositiveSmallIntegerField(verbose_name=_("ELO"), null=True, blank=True)

    family = models.ForeignKey(
        Family, on_delete=models.PROTECT, related_name="members",
        null=True, blank=True, verbose_name=_("Famille")
    )


class Committee(models.Model):

    class Meta:
        verbose_name = _("Comité")
        verbose_name_plural = _("Comités")

    name = models.CharField(_("Nom du comité"), max_length=256)

    def __str__(self):
        return self.name


class Member(Person):

    class Meta:
        verbose_name = _("Membre exécutif")
        verbose_name_plural = _("Membres exécutifs")
        ordering = ("role", "user")

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_("Utilisateur associé")
    )
    role = models.CharField(
        _("Fonction"), max_length=64, default="member",
        choices=club_settings.MEMBER_ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"


class CommitteeMember(Person):

    class Meta:
        verbose_name = _("Membre de comité")
        verbose_name_plural = _("Membres de comités")

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_("Utilisateur associé")
    )
    player = models.ForeignKey(
        Player, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_("Personne")
    )
    committee = models.ForeignKey(
        Committee, on_delete=models.PROTECT, verbose_name=_("Comité"),
        related_name="members"
    )
    role = models.CharField(
        _("Fonction"), max_length=64, default="member",
        choices=club_settings.COMMITTEE_MEMBER_ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"

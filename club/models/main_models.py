import os

from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

    def update_sold(self):
        from club.models import Payment, Expense
        total_payments = Payment.objects.aggregate(
            total_payments=models.Sum("amount")
        )["total_payments"] or 0
        total_expenses = Expense.objects.aggregate(
            total_expenses=models.Sum("amount")
        )["total_expenses"] or 0

        new_sold = total_payments - total_expenses
        self.sold = new_sold
        return self.save(update_fields=["sold"])

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

    def send_by_email(self, recipient, base_url="localhost:8000"):
        html_template = "club/email/book_download.html"
        html_body = render_to_string(
            html_template, {
                "book": self,
                "base_url": base_url
            }
        )
        body = strip_tags(html_body)
        platform_name = getattr(
            settings,
            "PLATFORM_NAME",
            "Ait Ourir Chess and Intelligence development Club (AOCID)"
        )
        email = EmailMultiAlternatives(
            subject=gettext("Votre lien de téléchargement est prêt - ") + f" {platform_name}",
            body=body,
            from_email="noreply@ekblocks.com",
            to=[recipient],
            headers={"Message-ID": f"download_book_{self.id}"},
        )
        email.attach_file(
            os.path.join(settings.MEDIA_ROOT, self.book_file.name)
        )
        email.attach_alternative(html_body, "text/html")
        try:
            email.send(
                fail_silently=False,
            )
            return True, _("Votre livre a été envoyé avec succès.")
        except Exception as e:
            return False, _(
                "Erreur d'envoi. Merci de verifier votre adresse email. "
                "Si elle est valid, prière de réessayer plus tard."
            )


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

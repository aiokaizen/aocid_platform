from django.db import models
from django.utils.translation import gettext_lazy as _, gettext

from club.models.main_models import Club, Subscription, Insurance
from club.models.person_models import Player


class Payment(models.Model):

    PAYMENT_TYPE = (
        ("", _("Non spécifié")),
        ("subscription_payment", _("Paiement d'adhésion")),
        ("insurance_payment", _("Paiement d'assurance")),
        ("donation", _("Un don")),
        ("other", _("Autre")),
    )

    class Meta:
        verbose_name = _("Paiement")
        verbose_name_plural = _("Paiements")

    amount = models.DecimalField(_("Montant"), max_digits=8, decimal_places=2)
    type_payment = models.CharField(
        _("Type de paiement"), max_length=32, default="", choices=PAYMENT_TYPE, blank=True
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_("Adhésion")
    )
    insurance = models.ForeignKey(
        Insurance, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_("Assurance")
    )
    player = models.ForeignKey(
        Player, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_("Adhérant")
    )
    donator = models.CharField(_("Donneur / Donneuse"), max_length=64, blank=True)
    reason = models.CharField(_("Motif"), max_length=256, blank=True, default="")
    anonyme = models.BooleanField(_("Anonyme"), default=False)
    payment_date = models.DateTimeField(_("Date de paiement"), auto_now_add=True)

    def __str__(self):
        if self.type_payment == "subscription_payment":
            return f"{self.amount} - {self.subscription}"
        elif self.type_payment == "insurance_payment":
            return f"{self.amount} - {self.player} - {self.insurance}"
        elif self.type_payment == "donation":
            return f"{self.amount} - {gettext('Don par')} {self.donator}"
        return f"{self.amount}"

    def save(self, *args, **kwargs):
        if self.type_payment == "donation" and not self.donator:
            self.donator = _("Anonyme")

        return super().save(*args, **kwargs)


class Expense(models.Model):

    class Meta:
        verbose_name = _("Dépense")
        verbose_name_plural = _("Dépenses")

    amount = models.DecimalField(_("Montant"), max_digits=8, decimal_places=2)
    reason = models.CharField(_("Motif"), max_length=256)
    expense_date = models.DateTimeField(_("Date de dépense"), auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.reason}"

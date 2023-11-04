import os

from django.core.files.storage import default_storage
from django.db.models import FileField, signals

from club.models import (
    Club, Payment, Expense
)


def post_save_update_sold(sender, **kwargs):
    """
    Update Club sold after Payments or Charges have been changed.
    """
    club = Club.get_club()
    club.update_sold()


def post_delete_update_sold(sender, **kwargs):
    return post_save_update_sold(sender, **kwargs)


### Connecting signals ###
# ---------------------- #

# Update sold attribute for Club
signals.post_save.connect(
    post_save_update_sold,
    sender=Payment,
    dispatch_uid="club.models.Payment.post_save_update_sold",
)
signals.post_delete.connect(
    post_delete_update_sold,
    sender=Payment,
    dispatch_uid="club.models.Payment.post_delete_update_sold",
)

signals.post_save.connect(
    post_save_update_sold,
    sender=Expense,
    dispatch_uid="club.models.Expense.post_save_update_sold",
)
signals.post_delete.connect(
    post_delete_update_sold,
    sender=Expense,
    dispatch_uid="club.models.Expense.post_delete_update_sold",
)

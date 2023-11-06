# Generated by Django 4.2.7 on 2023-11-04 18:51

import club.models.main_models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0014_committee_alter_member_options_alter_player_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Date et heure de départ",
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        default=club.models.main_models.get_now_plus_one_hour,
                        verbose_name="Date et heure de fin",
                    ),
                ),
                (
                    "absence_list",
                    models.ManyToManyField(
                        blank=True, to="club.player", verbose_name="Liste des absences"
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="club.plan",
                        verbose_name="Abonnement",
                    ),
                ),
            ],
            options={
                "verbose_name": "Seance",
                "verbose_name_plural": "Seances",
            },
        ),
    ]
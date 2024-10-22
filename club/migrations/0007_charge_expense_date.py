# Generated by Django 4.2 on 2023-11-02 16:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0006_payment_payment_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="charge",
            name="expense_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Date de dépense",
            ),
            preserve_default=False,
        ),
    ]

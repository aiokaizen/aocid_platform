# Generated by Django 4.2 on 2023-11-02 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0009_alter_player_options_payment_reason_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="anonyme",
            field=models.BooleanField(default=False, verbose_name="Anonyme"),
        ),
    ]
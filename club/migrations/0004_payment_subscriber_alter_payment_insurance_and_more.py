# Generated by Django 4.2 on 2023-10-30 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0003_member_role_payment_insurance_alter_member_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="subscriber",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="club.subscriber",
                verbose_name="Adhérant",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="insurance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="club.insurance",
                verbose_name="Assurance",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="subscription",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="club.subscription",
                verbose_name="Adhésion",
            ),
        ),
    ]

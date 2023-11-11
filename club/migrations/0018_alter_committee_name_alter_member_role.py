# Generated by Django 4.2.7 on 2023-11-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0017_alter_member_options_alter_committeemember_committee_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="committee",
            name="name",
            field=models.CharField(max_length=256, verbose_name="Nom du comité"),
        ),
        migrations.AlterField(
            model_name="member",
            name="role",
            field=models.CharField(
                choices=[
                    ("1_president", "Président"),
                    ("2_vice_president", "Vice président"),
                    ("3_secretary_general", "Secrétaire générale"),
                    ("4_vice_secretary_general", "Vice secrétaire générale"),
                    ("5_treasurer", "Trésorier"),
                    ("6_vice_treasurer", "Vice trésorier"),
                    ("7_council_member", "Conseiller"),
                ],
                default="member",
                max_length=64,
                verbose_name="Fonction",
            ),
        ),
    ]
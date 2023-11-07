# Generated by Django 4.2.7 on 2023-11-07 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0016_alter_session_options_alter_committeemember_role_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="member",
            options={
                "ordering": ("role", "user"),
                "verbose_name": "Membre exécutif",
                "verbose_name_plural": "Membres exécutifs",
            },
        ),
        migrations.AlterField(
            model_name="committeemember",
            name="committee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="members",
                to="club.committee",
                verbose_name="Comité",
            ),
        ),
        migrations.AlterField(
            model_name="committeemember",
            name="role",
            field=models.CharField(
                choices=[
                    ("coordinator", "Coordinateur"),
                    ("coordinator_f", "Coordinatrice"),
                    ("deputy", "Adjoint"),
                ],
                default="member",
                max_length=64,
                verbose_name="Fonction",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="role",
            field=models.CharField(
                choices=[
                    ("1_president", "Président"),
                    ("2_vice_president", "Vice président"),
                    ("3_secretary_general", "Secrétaire générale"),
                    ("4_treasurer", "Trésorier"),
                    ("5_vice_secretary_general", "Vice secrétaire générale"),
                    ("6_vice_treasurer", "Vice trésorier"),
                    ("7_council_member", "Conseiller"),
                ],
                default="member",
                max_length=64,
                verbose_name="Fonction",
            ),
        ),
    ]

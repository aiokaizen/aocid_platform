# Generated by Django 4.2.7 on 2023-11-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0006_alter_slide_alignment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slide",
            name="title",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="Title"
            ),
        ),
    ]

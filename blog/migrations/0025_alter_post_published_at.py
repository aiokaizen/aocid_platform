# Generated by Django 4.2.7 on 2023-11-07 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0024_alter_post_published_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 11, 7, 13, 36, 51, 141223),
                null=True,
                verbose_name="Published at",
            ),
        ),
    ]

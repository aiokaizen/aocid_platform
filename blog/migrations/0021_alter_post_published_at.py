# Generated by Django 4.2.7 on 2023-11-04 17:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0020_alter_post_published_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 11, 4, 18, 17, 14, 927091),
                null=True,
                verbose_name="Published at",
            ),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-03 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0015_alter_post_published_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 11, 3, 20, 28, 32, 176043),
                null=True,
                verbose_name="Published at",
            ),
        ),
    ]

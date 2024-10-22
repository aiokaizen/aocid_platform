# Generated by Django 4.2 on 2023-11-02 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_comment_ip_address_alter_post_published_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 11, 2, 15, 54, 17, 486278),
                null=True,
                verbose_name="Published at",
            ),
        ),
    ]

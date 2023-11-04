# Generated by Django 4.2 on 2023-11-02 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_remove_comment_verified_comment_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="ip_address",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="IP address"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 11, 2, 15, 54, 7, 513065),
                null=True,
                verbose_name="Published at",
            ),
        ),
    ]
# Generated by Django 4.2 on 2023-11-02 14:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_alter_comment_reply_to_alter_post_published_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="verified",
        ),
        migrations.AddField(
            model_name="comment",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "En Attend"),
                    ("accepted", "Accepté"),
                    ("denied", "Rejeté"),
                ],
                default="pending",
                max_length=32,
                verbose_name="Statut",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2023, 11, 2, 15, 33, 23, 471571),
                null=True,
                verbose_name="Published at",
            ),
        ),
    ]
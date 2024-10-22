# Generated by Django 4.2 on 2023-11-01 12:32

import autoslug.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import website.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=50, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="Last Name"),
                ),
                (
                    "birthday",
                    models.DateField(blank=True, null=True, verbose_name="Birthday"),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="E-mail")),
                (
                    "cv",
                    models.FileField(upload_to="website/cv_files/", verbose_name="Cv"),
                ),
                ("message", models.TextField(blank=True, verbose_name="Message")),
                (
                    "sent_by_mail",
                    models.BooleanField(default=False, verbose_name="Sent by mail"),
                ),
            ],
            options={
                "verbose_name": "Application",
                "verbose_name_plural": "Applications",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="Name")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="name"),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "unique_together": {("slug", "content_type")},
            },
        ),
        migrations.CreateModel(
            name="Counter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "icon",
                    models.FileField(
                        upload_to="website/counters/icons",
                        validators=[website.validators.validate_file_extension],
                        verbose_name="Icon",
                    ),
                ),
                ("count_to", models.IntegerField(default=0, verbose_name="Count To")),
            ],
            options={
                "verbose_name": "Counter",
                "verbose_name_plural": "Counters",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="", max_length=255, verbose_name="Full name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(default="", max_length=254, verbose_name="Email"),
                ),
                ("message", models.TextField(default="", verbose_name="Message")),
                (
                    "sent_by_mail",
                    models.BooleanField(default=False, verbose_name="Sent by mail"),
                ),
                (
                    "sent_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Sent date"),
                ),
            ],
            options={
                "verbose_name": "Message",
                "verbose_name_plural": "Messages",
            },
        ),
        migrations.CreateModel(
            name="NewsLetter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="Nom")),
                (
                    "emails",
                    models.JSONField(default=list, verbose_name="Liste des e-mails"),
                ),
            ],
            options={
                "verbose_name": "NewsLetter",
                "verbose_name_plural": "NewsLetters",
            },
        ),
        migrations.CreateModel(
            name="Slide",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "image",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        upload_to="website/sliders/images/", verbose_name="Image"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "alignment",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("left", "Left"),
                            ("center", "Center"),
                            ("right", "Right"),
                        ],
                        default="center",
                        max_length=255,
                        null=True,
                        verbose_name="Alignment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Slide",
                "verbose_name_plural": "Slides",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="Name")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                (
                    "short_description",
                    models.CharField(max_length=256, verbose_name="Short Description"),
                ),
                (
                    "image",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        upload_to="website/projects/projects_images/",
                        verbose_name="Image",
                    ),
                ),
                (
                    "published_at",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="Published_at"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created_at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated_at"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects",
                        to="website.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
            },
        ),
        migrations.CreateModel(
            name="Button",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("action", models.URLField(verbose_name="URL")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("video", "video"),
                            ("internal link", "internal link"),
                            ("external link", "external link"),
                        ],
                        max_length=255,
                        verbose_name="Type",
                    ),
                ),
                (
                    "slide",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buttons",
                        to="website.slide",
                    ),
                ),
            ],
            options={
                "verbose_name": "Button",
                "verbose_name_plural": "Buttons",
            },
        ),
    ]

import logging
import requests
from hashlib import sha256
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from autoslug import AutoSlugField
from image_cropping import ImageRatioField
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.


class Author(models.Model):
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = ThumbnailerImageField(
        _("Avatar"),
        upload_to="blog/authors/avatars",
        null=True,
        blank=True,
    )
    profession = models.CharField(
        _("Profession"), max_length=256, null=True, blank=True
    )
    description = models.TextField(
        _("Description"), null=True, blank=True, max_length=256
    )
    facebook = models.CharField(_("Facebook"), null=True, blank=True, max_length=256)
    instagram = models.CharField(_("Instagram"), null=True, blank=True, max_length=256)
    dribbble = models.CharField(_("Dribble"), null=True, blank=True, max_length=256)
    twitter = models.CharField(_("Twitter"), null=True, blank=True, max_length=256)
    youtube = models.CharField(_("Youtube"), null=True, blank=True, max_length=256)

    def __str__(self):
        return self.user.username

    def create(self):
        self.save()

    def get_posts(self):
        return Post.objects.filter(author=self)


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(verbose_name="Name", max_length=256)
    description = models.TextField(_("Description"), null=True, blank=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name

    def create(self):
        self.save()

    def get_posts(self):
        return Post.list(categories=self)

    @classmethod
    def list(cls, *args, **kwargs):
        return Category.objects.all()


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(_("Name"), max_length=256)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name

    def create(self):
        self.save()

    def get_posts(self):
        return Post.list(tags=self)

    @classmethod
    def list(cls, *args, **kwargs):
        return Tag.objects.all()


class Post(models.Model):

    class Meta:
        ordering = ("-published_at", "-created_at")
        permissions = (("can_publish_post", "Can publish post"),)

    title = models.CharField(verbose_name="Title", max_length=256)
    slug = AutoSlugField(populate_from="title", unique=True)
    short_description = models.TextField(verbose_name="Short description")
    content = RichTextUploadingField(verbose_name="Content")
    categories = models.ManyToManyField(
        Category, verbose_name="Categories", blank=True
    )
    tags = models.ManyToManyField(Tag)
    image = ThumbnailerImageField(
        verbose_name="Image",
        upload_to="blog/posts_images/",
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        Author, verbose_name="Author", on_delete=models.PROTECT, null=True, blank=True
    )
    published_at = models.DateTimeField(
        verbose_name="Published at", null=True, blank=True, default=datetime.now()
    )
    created_at = models.DateTimeField(
        verbose_name="Created at", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at", auto_now=True
    )

    def __str__(self):
        return f"{self.title}"

    def get_comments_count(self):
        return Comment.list(post=self, status="accepted").count()

    def get_comments(self):
        return Comment.list(post=self, status="accepted")

    # show published posts
    @classmethod
    def list(cls, show_unpublished=False, last_3_posts=False, last_4_posts=False, searching_text=None , *args, **kwargs):
        filters = {}
        if not show_unpublished:
            filters["published_at__lte"] = timezone.now()
            if last_3_posts:
                return Post.objects.filter(*args, **filters, **kwargs).order_by("-published_at")[:3]
            if last_4_posts:
                return Post.objects.filter(*args, **filters, **kwargs).order_by("-published_at")[:4]
            if searching_text:
                filters["title__startswith"] = searching_text
        return Post.objects.filter(*args, **filters, **kwargs)

    def create(self, user):
        can_create, msg = self.can_create()
        if not can_create:
            return False, msg

        self.author = user.author
        self.created_at = timezone.now()
        self.save()
        return True, "The post has been successfully inserted."

    def update(self, user):
        can_update, msg = self.can_update()
        if not can_update:
            return False, msg

        self.save()
        return True, "The post has been successfully updated."

    def publish(self, user):
        can_publish, msg = self.can_publish()
        if not can_publish:
            return False, msg

        self.published_at = timezone.now()

        self.save()
        return True, "The post has been successfully published."

    def unpublish(self, user):
        can_unpublish, msg = self.can_unpublish(user)
        if not can_unpublish:
            return False, msg

        self.published_at = None

        self.save()
        return True, "The post has been successfully returned to draft mode."

    def can_publish(self, user):
        if not user.hasperm("can_publish_post"):
            return False, "You don't have the required permissions to publish this post"
        return True, ""

    def can_unpublish(self, user):
        if not user.hasperm("can_unpublish_post"):
            return (
                False,
                "You don't have the required permissions to unpublish this post",
            )
        return True, ""

    def can_create(self, user):
        if not hasattr(user, "author"):
            return False, "You don't have the necessary permissions to create a post"
        return True, ""

    def can_update(self, user):
        if not hasattr(user, "author") or user.author != self.author:
            return False, "You don't have the necessary permissions to update this post"
        return True, ""


class Comment(models.Model):

    status_choices = (
        ("pending", _("En Attend")),
        ("accepted", _("Accepté")),
        ("denied", _("Rejeté")),
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(_("Email"), null=True, blank=True)
    ip_address = models.CharField(verbose_name="IP address", max_length=32, blank=True, null=True)
    content = models.TextField(_("Content"))
    rating = models.PositiveSmallIntegerField(
        _("Rating"), null=True, blank=True,
        help_text=_("Rate this post from 1 to 5")
    )
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="comments")
    published_at = models.DateTimeField(_("Publication date"), auto_now=True)
    reply_to = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="replies"
    )
    status = models.CharField(
        _("Statut"), max_length=32, default="pending", choices=status_choices
    )

    def __str__(self):
        if self.user:
            return f"{ self.user.first_name } { self.user.last_name }"
        else:
            return f"{self.email}"

    def exceeded_max_comments(self):
        id_filters = Q(ip_address=self.ip_address) | Q(email=self.email)
        interval = datetime.now() - timedelta(hours=10)
        old_messages = Comment.objects.filter(id_filters, published_at__gt=interval)
        return old_messages.count() > 10

    def get_gravatar_profile(self):
        email_hash = sha256(
            self.email.strip().lower().encode()
        ).hexdigest()

        # Get avatar only.
        # result = requests.get(f"https://gravatar.com/avatar/{email_hash}")

        # Get user profile
        result = requests.get(f"https://gravatar.com/{email_hash}.json")

        if result.status_code != 200:
            return None

        profile = result.json().get("entry")[0]

        data = {
            "thumbnail": profile["thumbnailUrl"],
            "name": profile["displayName"]
        }

        return data

    def can_create_comment(self):
        if self.exceeded_max_comments():
            return False, "You have exceeded the maximum number of allowed messages."
        return True, ""

    def create(self):

        can_create, msg = self.can_create_comment()
        if not can_create:
            return False, msg

        self.save()
        return True, ""

    @classmethod
    def list(cls, *args, **kwargs):
        return Comment.objects.filter(*args, **kwargs)

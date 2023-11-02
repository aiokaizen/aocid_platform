from django.contrib import admin
from blog.models import Author, Post, Category, Tag, Comment
from image_cropping import ImageCroppingMixin

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["user", "avatar", "profession"]
    fields = [
        "user",
        "avatar",
        "profession",
        "description",
        "facebook",
        "instagram",
        "dribbble",
        "twitter",
        "youtube",
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "slug"]
    fields = ["name", "description"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    fields = ["name"]


@admin.register(Post)
class PostAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = [
        "title",
        "short_description",
        # "categories",
        "author",
    ]

    fields = [
        "title",
        "image",
        "author",
        "short_description",
        "content",
        "categories",
        "tags",
        "published_at",
        "created_at",
        "updated_at",
    ]

    readonly_fields = ["created_at", "updated_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "status",
        "published_at",
        # "post",
    ]
    list_filter = [
        "status",
        "post",
        "user"
    ]
    fields = [
        "user",
        "email",
        # "ip_address",
        "content",
        "rating",
        "post",
        "published_at",
        "reply_to",
        "status"
    ]
    readonly_fields = (
        "published_at",
    )

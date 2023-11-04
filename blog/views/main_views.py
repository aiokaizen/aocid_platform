import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.http.response import JsonResponse
from blog.models import Post, Category, Tag, Comment, Author
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from website.utils import get_ip_address


class Blog(View):
    def get(self, request, category=None, tag=None):
        if category is not None:
            # all posts by category
            category = Category.objects.get(slug=category)
            posts = category.get_posts()
        elif tag is not None:
            # all posts by tag
            tag = Tag.objects.get(slug=tag)
            posts = tag.get_posts()
        else:
            # all published posts
            posts = Post.list()

        # last 3 posts
        last_posts = Post.list(last_3_posts=True)

        # all categories
        categories = Category.list()

        # all tags
        tags = Tag.list()

        context = {
            "title": _("Blog - Ait Ourir Chess Club"),
            "current_page": "blog",
            "posts": posts,
            "last_posts": last_posts,
            "categories": categories,
            "tags": tags,
            "category_filter": category,
            "tag_filter": tag,
        }
        return render(request, "blog/sandbox/blog.html", context)

    def post(self, request):
        searching_text = request.POST.get("title", "")
        posts = Post.list(searching_text=searching_text)
        last_posts = Post.list(last_3_posts=True)
        categories = Category.list()
        tags = Tag.list()
        context = {
            "title": _("Blog - Ait Ourir Chess Club"),
            "posts": posts,
            "last_posts": last_posts,
            "categories": categories,
            "tags": tags,
        }
        return render(request, "blog/sandbox/blog.html", context)


class BlogPost(View):

    def get(self, request, post):
        post = Post.objects.get(slug=post)

        # all comments of this post
        comments = post.get_comments()

        # all posts of the same category
        like_also = Post.list(categories__in=post.categories.all()).distinct().exclude(
            pk=post.pk
        )

        context = {
            "title": post.title,
            "current_page": "blog",
            "post": post,
            "like_also": like_also,
            "comments": comments,
        }
        return render(request, "blog/sandbox/blog_post.html", context)

    def post(self, request, post):
        success = False
        message = _("Please fix the errors below and try again")
        email = request.POST.get("email", "")
        content = request.POST.get("content", "")
        ip_address = get_ip_address(request)
        rating = None
        user = None
        try:
            user = User.objects.get(email=email)
        except:
            pass

        post = Post.objects.get(slug=post)
        comment = Comment(
            user=user,
            email=email,
            post=post,
            ip_address=ip_address,
            content=content,
            rating=rating,
        )
        success, msg = comment.create()
        if not success:
            message = msg
            success = False

        message = _("Your comment has been sent successfully. Once it is verified by one of our admins it will be displayed publically.")
        success = True

        return JsonResponse({"success": success, "message": message})

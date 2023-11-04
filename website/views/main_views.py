import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.http.response import JsonResponse
from django.contrib import messages

from website.forms import MessageForm, NewsLetterForm, ApplicationForm
from website.models import Counter, Slide
from website.models import *

from blog.models import Post

from club.models import (
    Book, Album, Media
)


class Home(View):

    def get(self, request):

        # Last 5 sliders
        sliders = Slide.objects.all().order_by("-id")[:5]

        # Last 4 counters
        counters = Counter.objects.all().order_by("-id")[:4]

        # Last 3 posts
        posts = Post.list(last_3_posts=True)

        # All published projects
        projects = Project.get_published_projects()

        # All projects categories
        categories = Category.objects.all()

        context = {
            "title": _("Home - Ait Ourir Chess Club"),
            "current_page": "home",
            "counters": counters,
            "sliders": sliders,
            "posts": posts,
            "projects": projects,
            "categories": categories,
        }

        return render(request, "website/home.html", context=context)

    def post(self, request):

        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("Your email has saved successfully")
            success = True
        else:
            message = _("Your email is not valid")
            success = False

        return JsonResponse({"success": success, "message": message})


class AboutUs(View):

    def get(self, request):
        context = {
            "title": _("About - Ait Ourir Chess Club"),
            "current_page": "about_us",
        }
        return render(request, "website/about_us.html", context)


class ContactUs(View):

    def get(self, request):
        context = {
            "title": _("Contact - Ait Ourir Chess Club"),
            "current_page": "contact_us",
        }
        return render(request, "website/contact_us.html", context=context)

    def post(self, request):
        form = MessageForm(request.POST)
        message = _("Please fix the errors below and try again")
        success = False
        if form.is_valid():
            try:
                form.save()
                message = _("Your message has been sent successfully. Thank you.")
                success = True
            except Exception as e:
                print("e:", e)
                message = _(
                    "An error occurred while trying to send your message. Please try again later."
                )

        return JsonResponse({"success": success, "message": message})


class Gallery(View):

    def get(self, request):

        albums = Album.objects.all()
        images = Media.objects.all()

        context = {
            "title": _("médiathèque - Ait Ourir Chess Club"),
            "current_page": "gallery",
            "albums": albums,
            "images": images,
        }
        return render(request, "website/gallery.html", context)


class BiblioChess(View):

    template_name = "website/biblio_chess.html"

    def get(self, request):

        books = Book.objects.all()

        context = {
            "title": _("Biblio-Chess - Ait Ourir Chess Club"),
            "current_page": "biblio_chess",
            "books": books
        }
        return render(request, self.template_name, context)

    def post(self, request):

        book_id = request.POST.get("book_id", 0)
        email = request.POST.get("email", None)
        book = get_object_or_404(Book, pk=book_id)

        if email is not None:
            base_url = request.build_absolute_uri("/")[:-1]
            success, msg = book.send_by_email(email, base_url)
            if success is False:
                messages.error(request, msg, extra_tags="danger")
            else:
                messages.success(request, msg)
        else:
            messages.error(request, _("Merci de fournir votre email."))

        books = Book.objects.all()
        context = {
            "title": _("Biblio-Chess - Ait Ourir Chess Club"),
            "current_page": "biblio_chess",
            "books": books
        }
        return render(request, self.template_name, context)


class Portfolio(View):

    def get(self, request):
        # Latest 6 projects
        last_6_projects = Project.get_latest_projects(6)

        # All published projects
        projects = Project.get_published_projects()

        context = {
            "title": _("Portfolio - Ait Ourir Chess Club"),
            "current_page": "portfolio",
            "last_6_projects": last_6_projects,
            "projects": projects,
        }
        return render(request, "website/portfolio.html", context)


class JoinUs(View):

    def get(self, request):
        context = {
            "title": _("Join Us - Ait Ourir Chess Club"),
            "current_page": "join_us",
        }
        return render(request, "website/join_us.html", context)

    def post(self, request):
        form = ApplicationForm(request.POST, request.FILES)
        message = _("Please fix the errors below and try again")
        success = False
        if form.is_valid():
            try:
                form.save()
                message = _("Your informations has been saved successfully. Thank you.")
                success = True
            except:
                message = _(
                    "An error occurred while trying to send your informations. Please try again later."
                )

        return JsonResponse({"success": success, "message": message})


class Terms(View):
    def get(self, request, element_id=None):
        context = {
            "title": _("Terms - Ait Ourir Chess Club"),
            "current_page": "join_us",
        }
        return render(request, "website/terms.html", context)


# ERROR HANDLERS
def handle_404_error(request, exception):
    return render(request, 'rogan/errors/404.html')


def handle_500_error(request):
    return render(request, 'rogan/errors/500.html')

from django.urls import include, path
from website import views

app_name = "website"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("about_us", views.AboutUs.as_view(), name="about_us"),
    path("contact_us", views.ContactUs.as_view(), name="contact_us"),
    path("gallery", views.Gallery.as_view(), name="gallery"),
    path("biblio_chess", views.BiblioChess.as_view(), name="biblio_chess"),

    path("terms", views.Terms.as_view(), name="terms"),

    path("portfolio", views.Portfolio.as_view(), name="portfolio"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

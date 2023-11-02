from django.urls import path, include
from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.Blog.as_view(), name="blog"),
    path("categories/<slug:category>/", views.Blog.as_view(), name="blog_category"),
    path("tags/<slug:tag>/", views.Blog.as_view(), name="blog_tag"),
    path("posts/<slug:post>/", views.BlogPost.as_view(), name="blog_post"),
]

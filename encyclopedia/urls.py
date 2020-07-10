from django.urls import path, re_path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^wiki/(?P<title>\w*)/$", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit")
]

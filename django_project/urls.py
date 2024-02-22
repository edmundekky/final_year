"""
URL configuration for django_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("profiler.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]

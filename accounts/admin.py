from django.contrib import admin
from .models import Investigator, Contact


@admin.register(Investigator)
class InvestigatorAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display_links = ("username", "email")
    search_fields = ("username", "email")
    ordering = ("username",)
    readonly_fields = ("date_joined", "last_login")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("subject", "message")
    ordering = ("created_at",)
    readonly_fields = ("created_at",)

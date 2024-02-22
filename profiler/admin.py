from django.contrib import admin
from profiler.models import (
    CyberCriminal,
    CyberCriminalMatch,
    Technique,
    Tactic,
    Alias,
    AssociatedIP,
    AssociatedDevice,
)


@admin.register(CyberCriminal)
class CyberCriminalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "d_o_b",
    )
    search_fields = ("name", "d_o_b", "height")


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "tactic")
    list_filter = ("tactic",)
    search_fields = ("name", "description")
    # limit the number of records displayed per page
    list_per_page = 10


@admin.register(Tactic)
class TacticAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name", "description")


@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ("cyber_criminal", "name")
    search_fields = ("cyber_criminal",)


@admin.register(AssociatedIP)
class AssociatedIPAdmin(admin.ModelAdmin):
    list_display = ("cyber_criminal", "ip_address")
    search_fields = ("cyber_criminal",)


@admin.register(AssociatedDevice)
class AssociatedDeviceAdmin(admin.ModelAdmin):
    list_display = ("cyber_criminal", "device_name")
    search_fields = ("cyber_criminal",)


@admin.register(CyberCriminalMatch)
class CyberCriminalMatchAdmin(admin.ModelAdmin):
    list_display = ("made_by", "number_of_techniques")
    list_filter = ("made_by",)
    search_fields = ("made_by",)

    # make a custom field for number of techniques used
    def number_of_techniques(self, obj):
        return obj.techniques.count()

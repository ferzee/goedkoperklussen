from django.contrib import admin
from .models import Sitemap


@admin.register(Sitemap)
class Sitemap(admin.ModelAdmin):
    fields = [
        'id',
        'store_name',
        'sitemap_name',
        'sitemap_url'
    ]

    list_display = [
        'id',
        'sitemap_name',
        'store_name'
    ]

    list_display_links = [
        'sitemap_name'
    ]

    readonly_fields = [
        'id'
    ]
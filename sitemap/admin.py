from django.contrib import admin
from .models import Sitemap


@admin.register(Sitemap)
class Sitemap(admin.ModelAdmin):
    fields = [
        'is_active',
        'id',
        'store_name',
        'sitemap_name',
        'sitemap_url'
    ]

    list_display = [
        'is_active',
        'id',
        'sitemap_name',
        'store_name',
        'sitemap_url'
    ]

    list_display_links = [
        'sitemap_name'
    ]

    readonly_fields = [
        'id'
    ]

    actions = [
        'set_active',
        'set_inactive'
    ]

    @admin.action(description='Set active')
    def set_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Set inactive')
    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)

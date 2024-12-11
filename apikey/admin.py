from django.contrib import admin
from .models import APIKey


@admin.register(APIKey)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'key',
        'created_at'
    ]

    readonly_fields = [
        'id',
        'created_at'
    ]

    list_display = [
        'id',
        'user'
    ]

    list_display_links = [
        'user'
    ]

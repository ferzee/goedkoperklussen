from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'activity_name',
        'activity_description',
        'created_at',
        'updated_at'
    ]

    list_display = [
        'id',
        'activity_name',
        'created_at',
        'updated_at'
    ]

    list_display_links = [
        'activity_name'
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at'
    ]

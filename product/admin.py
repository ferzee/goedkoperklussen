from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'product_name',
        'store_name',
        'product_url',
        'price',
        'updated_at'
    ]

    list_display = [
        'id',
        'product_name',
        'store_name',
        'price',
        'updated_at'
    ]

    list_display_links = [
        'product_name'
    ]

    readonly_fields = [
        'id',
        'updated_at'
    ]

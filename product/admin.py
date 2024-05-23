from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'product_name',
        'product_category',
        'store_name',
        'original_price',
        'discount_price',
        'product_url',
        'is_discounted',
        'last_updated'
    ]

    list_display = [
        'id',
        'product_name',
        'product_category',
        'is_discounted'
    ]

    list_display_links = [
        'product_name'
    ]

    readonly_fields = [
        'id',
        'discount_amount'
    ]


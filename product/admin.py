from django.contrib import admin
from .models import Product, ProductPriceLine


class ProductPriceLineInline(admin.TabularInline):
    model = ProductPriceLine
    extra = 0  # No extra empty forms by default
    readonly_fields = ("price", "date")  # Make fields read-only for existing entries


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'product_name',
        'store_name',
        'product_url',
        'current_price',
        'previous_price',
        'is_discounted',
        'updated_at'
    ]

    list_display = [
        'id',
        'product_name',
        'store_name',
        'current_price',
        'previous_price',
        'is_discounted',
        'updated_at'
    ]

    list_display_links = [
        'product_name'
    ]

    readonly_fields = [
        'id',
        'updated_at',
        'previous_price',
        'is_discounted'
    ]

    inlines = [ProductPriceLineInline]  # Include the inline for ProductPriceLine


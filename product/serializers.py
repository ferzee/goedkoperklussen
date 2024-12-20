from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=255)
    product_description = serializers.CharField(allow_blank=True)
    ean_code = serializers.CharField(max_length=20, allow_blank=True)
    store_name = serializers.CharField(max_length=100)
    current_price = serializers.FloatField()
    product_url = serializers.URLField()
    img_url = serializers.URLField(allow_blank=True)

    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'ean_code', 'store_name', 'current_price', 'product_url', 'img_url']
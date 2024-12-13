from rest_framework import serializers
from .models import Sitemap

class SitemapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitemap
        fields = '__all__'
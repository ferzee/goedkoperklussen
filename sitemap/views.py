from django.shortcuts import render
from apikey.authentication import APIKeyAuthentication
from rest_framework import viewsets
from .models import Sitemap
from .serializers import SitemapSerializer

class SitemapViewSet(viewsets.ModelViewSet):
    permission_classes = [APIKeyAuthentication]

    queryset = Sitemap.objects.all()
    serializer_class = SitemapSerializer


from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SitemapViewSet

router = DefaultRouter()
router.register(r'sitemaps', SitemapViewSet)

urlpatterns = []

urlpatterns += router.urls  # Add the router-generated URLs

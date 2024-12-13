from django.urls import path

from . import views

router = DefaultRouter()
router.register(r'sitemaps', SitemapViewSet)

urlpatterns = []

urlpatterns += router.urls  # Add the router-generated URLs

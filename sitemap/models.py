from django.db import models


class Sitemap(models.Model):
    store_name = models.CharField(max_length=50)
    sitemap_name = models.CharField(max_length=50)
    sitemap_url = models.CharField(max_length=100)

    def __str__(self):
        return self.sitemap_name
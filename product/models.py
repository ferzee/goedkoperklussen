from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    # Add product_uom = models.CharField(max_length=100)
    product_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO
    # - Add category for easier lookup
    # - Add price comparison via a table of prices with date, so we can provide a price progression graph

    def __str__(self):
        return self.product_name

from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    product_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.product_name

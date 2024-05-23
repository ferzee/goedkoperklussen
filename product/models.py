from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    original_price = models.FloatField(default=0.0)
    discount_price = models.FloatField(default=0.0)
    discount_amount = models.FloatField(default=0.0)
    product_url = models.CharField(max_length=100)
    is_discounted = models.BooleanField()
    last_updated = models.DateField()

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.discount_amount = self.original_price - self.discount_price

        if self.discount_amount > 0.0:
            self.is_discounted = True
        else:
            self.is_discounted = False

        super().save(*args, **kwargs)

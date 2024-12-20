from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    store_name = models.CharField(max_length=100)
    ean_code = models.CharField(max_length=20, null=True, blank=True)
    current_price = models.FloatField(default=0.0)
    previous_price = models.FloatField(default=0.0, editable=False)
    is_discounted = models.BooleanField(default=False, editable=False)
    product_uom = models.CharField(max_length=100, null=True, blank=True)
    product_url = models.CharField(max_length=255, null=True, blank=True)
    img_url = models.CharField(max_length=255, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not is_new:
            original = Product.objects.get(pk=self.pk)
            if original.current_price != self.current_price:
                self.previous_price = original.current_price
                self.is_discounted = self.current_price < original.current_price
        else:
            self.previous_price = self.current_price

        super().save(*args, **kwargs)

        if self.pk:
            ProductPriceLine.objects.create(product=self, price=self.current_price)


class ProductPriceLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_lines")
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.price} on {self.date}"

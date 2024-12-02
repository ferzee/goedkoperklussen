from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    current_price = models.FloatField(default=0.0)
    previous_price = models.FloatField(default=0.0, editable=False)  # Auto-filled, not editable directly
    is_discounted = models.BooleanField(default=False, editable=False)  # Auto-updated, not editable directly
    product_uom = models.CharField(max_length=100)
    product_url = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO
    # - Add category for easier lookup
    # - Add price comparison via a table of prices with date, so we can provide a price progression graph

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the product exists
            original = Product.objects.get(pk=self.pk)
            if original.current_price != self.current_price:
                self.previous_price = original.current_price  # Set the previous price
                self.is_discounted = self.current_price < self.previous_price  # Check if discounted
                # Record the price change in ProductPriceLine
                ProductPriceLine.objects.create(product=self, price=self.current_price)
        else:
            # For new products, initialize previous_price and create the first price line
            self.previous_price = self.current_price
            ProductPriceLine.objects.create(product=self, price=self.current_price)
        super().save(*args, **kwargs)


class ProductPriceLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_lines")
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.price} on {self.date}"

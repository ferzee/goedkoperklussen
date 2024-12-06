"""

This action removes all products that haven't been updated in the past week.
That means these products couldn't be found and should therefore not be displayed
on the website.

"""

import django
import os
import datetime
from django.utils import timezone  # Import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goedkoperklussen.settings')
django.setup()

from product.models import Product


current_date = timezone.now()

days_not_updated = 7
check_date = current_date - datetime.timedelta(days=days_not_updated)

products = Product.objects.all()

delete_count = 0

for product in products:
    if product.updated_at < check_date:
        product.delete()
        delete_count += 1

print(f'Deleted {delete_count} records')
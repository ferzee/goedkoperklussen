from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template import loader

from .models import Product


def index(request):
    products = Product.objects.filter(current_price__gt=0.0)
    context = {
        "products": products,
    }

    return render(request, "product/products.html", context)

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template import loader

from .models import Product


def index(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }

    return render(request, "product/products.html", context)

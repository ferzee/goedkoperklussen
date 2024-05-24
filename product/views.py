from django.http import HttpResponse
from django.template import loader

from .models import Product

def index(request):
    product_list = Product.objects.all()
    template = loader.get_template("product/products.html")
    context = {
        "product_list" : product_list,
    }

    return HttpResponse(template.render(context, request))
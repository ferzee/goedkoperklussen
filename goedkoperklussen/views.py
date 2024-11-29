from django.shortcuts import render
from django.db.models import Q
from product.models import Product


def search_results(request):
    query = request.GET.get('q')

    products = Product.objects.filter(
        Q(product_name__icontains=query)
    )

    context = {
        'products': products,
    }

    return render(request, 'search_results.html', context)

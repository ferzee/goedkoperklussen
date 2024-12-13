from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from product.models import Product
from django.template.loader import render_to_string


def search_results(request):
    query = request.GET.get('q')
    page_number = int(request.GET.get("page", 1))  # Default to page 1

    query_words = query.split()

    search_filter = Q()

    for word in query_words:
        search_filter &= Q(product_name__icontains=word)

    # Filter products based on the search query
    products = Product.objects.filter(search_filter).order_by('-updated_at')

    # Pagination setup
    paginate_by = 48
    paginator = Paginator(products, paginate_by)
    page_obj = paginator.get_page(page_number)

    # Check if this is the last page
    is_last_page = not page_obj.has_next()

    # Handle partial vs. full response
    if request.GET.get("page"):
        # Render partial for pagination
        return render(request, 'partials/search_results_products.html', {
            'page_obj': page_obj,
            'query': query,
            'is_last_page': is_last_page,
        })

    # Render full page for initial request
    context = {"page_obj": page_obj, 'query': query, 'is_last_page': is_last_page}
    return render(request, 'search_results.html', context)
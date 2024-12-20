from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from apikey.authentication import APIKeyAuthentication
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string


def index(request):
    products = Product.objects.filter(current_price__gt=0.0).order_by('-created_at')

    paginate_by = 48
    paginator = Paginator(products, paginate_by)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('HX-Request'):
        html = render_to_string('partials/products.html', {'page_obj': page_obj}, request)
        return HttpResponse(html)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'product/products.html', context)


def other_stores(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.ean_code:
        related_products = Product.objects.filter(ean_code=product.ean_code).exclude(pk=product.id)
    else:
        related_products = []

    context = {
        'product': product,
        'related_products': related_products
    }

    return render(request, 'product/other_stores.html', context)


class ProductCreateView(APIView):
    authentication_classes = [APIKeyAuthentication]  # Require API Key authentication

    @staticmethod
    def upsert_product(product_name, product_description, ean_code, store_name, price, url, img_url):
        try:
            # Use url as an unique identifier.
            product = Product.objects.get(product_url=url)
            product.name = product_name
            product.description = product_description
            ean_code = ean_code
            product.store_name = store_name
            product.current_price = price
            product.img_url = img_url

            product.save()
            print(f"Product {product_name} updated. url: {url}")

        except ObjectDoesNotExist:
            new_product = Product(
                name=product_name,
                description=product_description,
                ean_code=ean_code,
                store_name=store_name,
                current_price=price,
                product_url=url,
                img_url=img_url
            )

            new_product.save()
            print(f"New product {product_name} created. url: {url}")

    def post(self, request):
        # Extract the list of products from the request
        products_data = request.data.get('products', [])

        if not products_data:
            return Response({"detail": "No products provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Iterate over each product and validate/update or create
        for product_data in products_data:
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Check if the product already exists, and update or create
                product, created = Product.objects.update_or_create(
                    product_url=validated_data.get("product_url"),
                    defaults={
                        "name": validated_data.get("product_name"),
                        "description": validated_data.get("product_description"),
                        "ean_code": validated_data.get("ean_code"),
                        "store_name": validated_data.get("store_name"),
                        "current_price": validated_data.get("current_price"),
                        "img_url": validated_data.get("img_url", ""),
                    },
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Products processed successfully"}, status=status.HTTP_200_OK)

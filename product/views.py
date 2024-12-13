from django.shortcuts import render
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
    # Fetch and paginate products
    products = Product.objects.filter(current_price__gt=0.0).order_by('-created_at')
    paginate_by = 48
    paginator = Paginator(products, paginate_by)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Check if this is an HTMX request
    if request.headers.get('HX-Request'):
        # Render only the product list HTML
        html = render_to_string('partials/products.html', {'page_obj': page_obj}, request)
        return HttpResponse(html)

    # Otherwise, render the full template
    context = {"page_obj": page_obj}
    return render(request, "product/products.html", context)


class ProductCreateView(APIView):
    authentication_classes = [APIKeyAuthentication]  # Require API Key authentication

    @staticmethod
    def upsert_product(product_name, store_name, price, url, img_url):
        try:
            # Use url as an unique identifier.
            product = Product.objects.get(product_url=url)
            product.product_name = product_name
            product.store_name = store_name
            product.current_price = price
            product.img_url = img_url

            product.save()
            print(f"Product {product_name} updated. url: {url}")

        except ObjectDoesNotExist:
            new_product = Product(
                product_name=product_name,
                store_name=store_name,
                current_price=price,
                product_url=url,
                img_url=img_url
            )

            new_product.save()
            print(f"New product {product_name} created. url: {url}")

    def post(self, request):
        # Extract data from the request
        product_data = request.data

        # Validate the incoming data using the serializer
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            # Extract validated data
            validated_data = serializer.validated_data
            # Use update_or_create directly in the view
            Product.objects.update_or_create(
                product_url=validated_data.get("product_url"),
                defaults={
                    "product_name": validated_data.get("product_name"),
                    "store_name": validated_data.get("store_name"),
                    "current_price": validated_data.get("current_price"),
                    "img_url": validated_data.get("img_url"),
                },
            )
            return Response({"message": "Product processed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

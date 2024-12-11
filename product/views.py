from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from apikey.authentication import APIKeyAuthentication


def index(request):
    products = Product.objects.filter(current_price__gt=0.0)
    context = {
        "products": products,
    }

    return render(request, "product/products.html", context)


class ProductCreateView(APIView):
    authentication_classes = [APIKeyAuthentication]  # Require API Key authentication

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new Product to the database
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


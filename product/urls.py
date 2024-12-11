from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path("", views.index, name="products"),
    path('api/products/create', views.ProductCreateView.as_view(), name='create-product'),
]

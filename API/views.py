from ecommerce.models import Product
from rest_framework import generics
from .serializers import ProductSerializer
# Create your views here.

class ProductsInStockList(generics.ListAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(stock__gt=1)

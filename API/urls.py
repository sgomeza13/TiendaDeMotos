from .views import ProductsInStockList
from django.urls import path

urlpatterns = [
    path("productsinstock",ProductsInStockList.as_view(),name='pinstock')
]
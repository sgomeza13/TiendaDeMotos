from django.urls import path 
from .views import HomeView, ProductCreateView, ProductListView, ProductView, ErrorView, ProductUpdateView, CartView, ClearCartView, CheckoutView

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("create/",ProductCreateView.as_view(),name='create'),
    path('products/',ProductListView.as_view(),name='products'),
    path('product/<str:id>',ProductView.as_view(),name='product'),
    path('error/',ErrorView.as_view(),name='error'),
    path('product/update/<pk>',ProductUpdateView.as_view(),name='updateproduct'),

    path('cart/', CartView.as_view(), name='cart'),
    path('clear-cart/', ClearCartView.as_view(), name='clear_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),


]

handler404 = ErrorView.as_view()
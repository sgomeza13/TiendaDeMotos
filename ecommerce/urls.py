from django.urls import path 
from .views import HomeView, ProductCreateView, ProductListView, ProductView, ErrorView, ProductUpdateView

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("create/",ProductCreateView.as_view(),name='create'),
    path('products/',ProductListView.as_view(),name='products'),
    path('product/<str:id>',ProductView.as_view(),name='product'),
    path('error/',ErrorView.as_view(),name='error'),
    path('product/update/<pk>',ProductUpdateView.as_view(),name='updateproduct')
]

handler404 = ErrorView.as_view()
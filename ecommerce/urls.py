from django.urls import path 
from .views import HomeView, ProductCreateView, RegisterView, LoginView, ProductListView, ProductView

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("create/",ProductCreateView.as_view(),name='create'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('products/',ProductListView.as_view(),name='products'),
    path('product/<str:id>',ProductView.as_view(),name='product')
]
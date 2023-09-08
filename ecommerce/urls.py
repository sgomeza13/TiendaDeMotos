from django.urls import path 
from .views import HomeView, ProductCreateView, RegisterView, LoginView

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("create/",ProductCreateView.as_view(),name='create'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
]
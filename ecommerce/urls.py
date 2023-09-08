from django.urls import path 
from .views import HomeView, ProductCreateView

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("create/",ProductCreateView.as_view(),name='create')
]
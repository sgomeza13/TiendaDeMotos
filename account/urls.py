from django.urls import path

from .views import RegisterView, LoginView, LogOutView 

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogOutView.as_view(),name='logout'),

]
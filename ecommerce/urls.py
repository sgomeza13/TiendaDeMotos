from django.urls import path, re_path 
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ProductCreateView, ProductListView, ProductView, ErrorView, ProductUpdateView
from django.views.static import serve

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("create/",ProductCreateView.as_view(),name='create'),
    path('products/',ProductListView.as_view(),name='products'),
    path('product/<str:id>',ProductView.as_view(),name='product'),
    path('error/',ErrorView.as_view(),name='error'),
    path('product/update/<pk>',ProductUpdateView.as_view(),name='updateproduct'),
    re_path(r'^products/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), #magia de chatgpt
    re_path(r'^product/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = ErrorView.as_view()

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
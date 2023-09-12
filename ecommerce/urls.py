from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ProductCreateView, ProductListView, ProductView, ErrorView, ProductUpdateView, CartView, ClearCartView, CheckoutView, PaypalView, OrdersListView, DeleteOrderView
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
    path('cart/', CartView.as_view(), name='cart'),
    path('clear-cart/', ClearCartView.as_view(), name='clear_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('paypal/', PaypalView.as_view(), name='paypal'),
    
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('delete_order/<int:order_id>/', DeleteOrderView.as_view(), name='delete_order')


]

handler404 = ErrorView.as_view()
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
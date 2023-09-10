from django.conf import settings
from django.db.models.query import QuerySet
from django.forms import TextInput
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView
from .forms import ProductForm
from .models import Product
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q

# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/home.html"


class ErrorView(TemplateView):
    template_name = "error.html"

class ProductCreateView(PermissionRequiredMixin,View):
    template_name = 'pages/createproduct.html'
    permission_required = 'auth.is_superuser'
    form = ProductForm()
    viewData = {}
    viewData["title"] = "Create product"
    viewData["form"] = form
    def get(self, request):
        return render(request, self.template_name, self.viewData)
    def post(self, request):
        form = ProductForm(request.POST)
        viewData = {}
        viewData["form"] = form
        print(form.data)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:

            return render(request, self.template_name, viewData)

class ProductUpdateView(PermissionRequiredMixin,UpdateView):
    model = Product
    permission_required = 'auth.is_superuser'
    template_name = "pages/update.html"
    fields = [
        "name",
        "reference",
        "stock",
        "price",
        "brand",
        "description"
    ]


    success_url = "/products"
        
class ProductListView(ListView):
    model = Product
    template_name = 'pages/products.html'
    context_object_name = "products"
    form = ProductForm()
    def get_queryset(self):
        query = self.request.GET.get("name")
        brand = self.request.GET.get("brand")
        minprice = self.request.GET.get("minprice")
        maxprice = self.request.GET.get("maxprice")
        if not query:
            query = ""
        if not brand:
            brand = ""
        if not minprice:
            minprice = 0
        if not maxprice:
            maxprice = 9999999999
        
        filters_query = Q(name__icontains=query) | Q(reference__icontains=query)  
        filters_query &= Q(brand__icontains=brand)
        filters_query &= Q(price__gte=minprice) & Q(price__lte=maxprice)
        products = Product.objects.filter(filters_query)
        return products
    #Obtiene los valores de las marcas del ProductForms para usarlos en el Select
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form  
        return context


class ProductView(View):
    template_name = 'pages/product.html'
    def get(self, request, id):
        viewData = {}
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except:
            return redirect('error')

        viewData["product"] = product
        
        return render(request, self.template_name, viewData)
    def post(self, request, id):
        if(request.POST.get('delete')):
            product = get_object_or_404(Product, pk=id)
            product.delete()
        return redirect('products')
    
    

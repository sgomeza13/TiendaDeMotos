from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View, CreateView
from .forms import ProductForm, CustomerForm, LoginForm, CustomerChangeForm
from .models import Product
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/home.html"
    def get(self, request):
        viewData={
            "isSuperUser":0
        }

        if(request.user.is_superuser):
            viewData['isSuperUser'] = 1
        return render(request, self.template_name, viewData)

class ErrorView(TemplateView):
    template_name = "error.html"

class ProductCreateView(LoginRequiredMixin,View):
    template_name = 'pages/createproduct.html'

    form = ProductForm()
    viewData = {}
    viewData["title"] = "Create product"
    viewData["form"] = form
    def get(self, request):
        if(request.user.is_superuser):
            return render(request, self.template_name, self.viewData)
        else:
            return redirect('error')
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
        
class ProductListView(ListView):
    model = Product
    template_name = 'pages/products.html'
    context_object_name = 'products'

class ProductView(View):
    template_name = 'pages/product.html'
    def get(self, request, id):
        viewData = {}
        if(request.user.is_superuser):
            viewData['isSuperUser'] = 1
        else:
            viewData['isSuperUser'] = 0

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
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return redirect('list')
    
    
class RegisterView(CreateView):
    template_name = 'pages/register.html'

    def get(self, request):
        form = CustomerForm()
        viewData = {}
        viewData['form'] = form
        return render(request,self.template_name, viewData)
    def post(self, request):
        form = CustomerForm(request.POST)
        viewData = {}
        viewData['form'] = form.data
        print(viewData['form'])
        if(form.is_valid()):
            form.save(commit=True)
            return redirect("home")
        else:
            viewErrors = {
                'form':form
            }
            return render(request, self.template_name, viewErrors)
        
class LoginView(View):
    template_name = 'pages/login.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        user = authenticate(request,username=request.POST['email'],password=request.POST['password'])
        print(user)
        if(user != None):
            login(request, user)
            return redirect('home')
        else:
            viewData = {}
            viewData["error"] = "Usuario o contraseña incorrectos"
             
            return render(request,self.template_name, viewData)

class LogOutView(View):
#def logout_view(request):
    def get(self, request):
        logout(request)
        return redirect('home')
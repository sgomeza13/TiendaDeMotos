from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from .forms import ProductForm
# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/home.html"


class ProductCreateView(View):
    template_name = 'pages/create.html'
    brands = ["Kawasaki","Honda","Yamaha","Suzuki"]
    form = ProductForm()
    viewData = {}
    viewData["title"] = "Create product"
    viewData["form"] = form
    viewData["brands"] = brands
    def get(self, request):

        return render(request, self.template_name, self.viewData)
    def post(self, request):
        form = ProductForm(request.POST)
        print(form.data)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:

            return render(request, self.template_name, self.viewData)
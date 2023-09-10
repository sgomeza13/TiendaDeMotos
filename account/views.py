from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView
from .forms import CustomerForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.

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
    def get(self, request):
        logout(request)
        return redirect('home')
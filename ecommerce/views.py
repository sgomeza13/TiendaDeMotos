from typing import Any
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View, UpdateView
from .forms import ProductForm, RatingForm, OrdersForm
from .models import Product, Rating, Orders
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
class HomeView(ListView):
    model = Product
    template_name = "pages/home.html"
    context_object_name = "products"

    def get_queryset(self):
        # Calcula el promedio de calificacion de todos los productos y los ordena de manera descendiente
        queryset = Rating.objects.annotate(average_rating=Avg('rating')).order_by('-average_rating')

        # Deja solo los primeros 3
        top_rated_products = queryset[:3]

        return top_rated_products


class PaypalView(TemplateView):
    template_name = "checkout/paypal.html"

    def get(self, request):
        # Retrieve cart items from the session
        cart_items = request.session.get('cart', [])

        # Calculate the total price of items in the cart
        total_price = 0

        products_in_cart = []

        for item in cart_items:
            try:
                product = Product.objects.get(reference=item['reference'])
                products_in_cart.append({
                    'nombre': product.name,
                    'referencia': product.reference,
                    'cantidad': item['quantity'],
                    'precio': product.price,
                })
                total_price += product.price * item['quantity']
            except Product.DoesNotExist:
                pass

        # Get the user information
        user = request.user

        context = {
            'cart_items': products_in_cart,
            'total_price': total_price,
            'user': user,
        }

        return render(request, self.template_name, context)


class ErrorView(TemplateView):
    template_name = "error.html"


class ProductCreateView(PermissionRequiredMixin, View):
    template_name = 'pages/createproduct.html'
    permission_required = 'auth.is_superuser'
    form = ProductForm()
    viewData = {}
    viewData["title"] = "Create product"
    viewData["form"] = form

    def get(self, request):
        return render(request, self.template_name, self.viewData)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        viewData = {}
        viewData["form"] = form
        print(form.data)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:

            return render(request, self.template_name, viewData)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'auth.is_superuser'
    template_name = "pages/update.html"
    form_class = ProductForm

    success_url = "/products/"


class ProductListView(ListView):
    model = Product.objects
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

    # Obtiene los valores de las marcas del ProductForms para usarlos en el Select
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class ProductView(View):
    template_name = 'pages/product.html'
    form = RatingForm
    viewData = {}
    viewData['form'] = form

    def get(self, request, id):

        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
            rating = Rating.objects.filter(product_id=product_id).aggregate(Avg("rating"))
            try:
                rating = round(rating.get('rating__avg'), 1)
            except:
                rating = 0
        except:
            return redirect('error')

        self.viewData["product"] = product
        self.viewData["rating"] = rating

        return render(request, self.template_name, self.viewData)

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if (request.POST.get('delete')):
            product.delete()
        elif (request.POST.get('rate')):
            form = RatingForm(request.POST)
            if form.is_valid():
                # Chequea si el usuario ya a calificado el producto anteriormente, si lo ha hecho, lo actualiza
                existing_rating = Rating.objects.filter(user=request.user, product=product).first()
                if existing_rating:
                    existing_rating.rating = form.cleaned_data['rating']
                    existing_rating.save()
                    url = f"/product/{id}"
                    return redirect(url)
                else:
                    rate = form.save(commit=False)
                    rate.user = request.user
                    rate.product = product
                    rate.save()

        return redirect('products')


class CartView(View):
    template_name = 'cart/cart.html'

    def get(self, request):
        cart_items = request.session.get('cart', [])
        products_in_cart = []

        # Retrieve product details based on product references in the cart
        for item in cart_items:
            try:
                product = Product.objects.get(reference=item['reference'])
                products_in_cart.append({
                    'nombre': product.name,
                    'referencia': product.reference,
                    'cantidad': item['quantity'],
                    'precio': product.price,
                })
            except Product.DoesNotExist:
                pass

        context = {
            'cart_items': products_in_cart,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        reference = request.POST.get('reference')
        quantity = int(request.POST.get('quantity', 1))

        # Retrieve the cart from the session or create an empty cart
        cart_items = request.session.get('cart', [])

        # Check if the product is already in the cart
        for item in cart_items:
            if item['reference'] == reference:
                # Update the quantity if the product is already in the cart
                item['quantity'] += quantity
                break
        else:
            # Add the product to the cart if not already present
            cart_items.append({

                'reference': reference,
                'quantity': quantity,
            })

        # Update the cart in the session
        request.session['cart'] = cart_items

        return redirect('cart')


class ClearCartView(View):
    def get(self, request):
        # Clear the cart session data
        request.session['cart'] = []
        return redirect('cart')


class CheckoutView(View):
    template_name = 'checkout/checkout.html'

    def get(self, request):
        # Retrieve cart items from the session
        cart_items = request.session.get('cart', [])

        # Calculate the total price of items in the cart
        total_price = 0

        products_in_cart = []

        for item in cart_items:
            try:
                product = Product.objects.get(reference=item['reference'])
                products_in_cart.append({
                    'nombre': product.name,
                    'referencia': product.reference,
                    'cantidad': item['quantity'],
                    'precio': product.price,
                })
                total_price += product.price * item['quantity']
            except Product.DoesNotExist:
                pass

        # Get the user information
        user = request.user

        context = {
            'cart_items': products_in_cart,
            'total_price': total_price,
            'user': user,  
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        if request.method == 'POST':
            form = OrdersForm(request.POST)  # Replace with your actual form class
            if form.is_valid():
                order = Orders(
                user=request.user if request.user.is_authenticated else None,
                name=form.cleaned_data['Nombre'],
                email=form.cleaned_data['Email'],
                city=form.cleaned_data['Ciudad'],
                address=form.cleaned_data['Direccion'],
                product=form.cleaned_data['product'],
                total_price=form.cleaned_data['total_price']
            )
            order.save()
            return redirect('paypal') 
        else:
            form = OrdersForm()  # Replace with your actual form class



class OrdersListView(View):
    template_name = 'orderlist/orders.html'

    def get(self, request):
        orders = Orders.objects.all()
        return render(request, self.template_name, {'orders': orders})

class DeleteOrderView(View):
    def get(self, request, order_id):
        try:
            order = Orders.objects.get(pk=order_id)
            order.delete()
        except Orders.DoesNotExist:
            # Handle the case where the order doesn't exist
            pass
        return redirect('orders')



        
        
    

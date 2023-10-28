from django import forms
from .models import Product, Rating

class ProductForm(forms.ModelForm):


    class Meta:
        model = Product
        fields = ['name','price', 'description','brand','stock', 'reference', 'image']
    BRAND_CHOICES = [
        ("","Sin Marca/Cualquier Marca"),
        ("Kawasaki", "Kawasaki"),
        ("Honda", "Honda"),
        ("Yamaha", "Yamaha"),
        ("Suzuki", "Suzuki"),
        
    ]

    brand = forms.ChoiceField(label="Brand", choices=BRAND_CHOICES, required=False)

    def clean_price(self):
        price = self.cleaned_data['price']
        if (price <= 0):
            raise forms.ValidationError("El precio debe ser mayor a cero")
        return price
    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if (stock <= 0):
            raise forms.ValidationError("Debe haber por lo menos 1 unidad")
        return stock

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
    RATING_CHOICES = [
        (1,"1 - Calidad Mala"),
        (2,"2 - Calidad Regular"),
        (3,"3 - Calidad Aceptable"),
        (4,"4 - Calidad Buena"),
        (5,"5 - Calidad Excelente"),
    ]
    rating = forms.ChoiceField(label="Rating",choices=RATING_CHOICES)


class OrdersForm(forms.Form):
    Nombre = forms.CharField(max_length=255)
    Email = forms.EmailField()
    Ciudad = forms.CharField(max_length=20)
    Direccion = forms.CharField(max_length=255)
    product = forms.CharField(max_length=255)
    total_price = forms.IntegerField(widget=forms.HiddenInput()) 


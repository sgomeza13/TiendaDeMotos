from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price', 'description','brand','stock']

    def clean_price(self):
        price = self.cleaned_data['price']
        if (price <= 0):
            raise forms.ValidationError("El precio debe ser mayor a cero")
        return price
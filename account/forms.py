from django import forms
from .models import CustomerUser


class CustomerForm(forms.ModelForm):

    class Meta:
        model = CustomerUser
        fields = ['email', 'password', 'first_name','last_name', 'address', 'city']
    
    CITY_CHOICES = [
        ("Medellin", "Medellin"),
        ("Bogota", "Bogota"),
        ("Manizales", "Manizales"),
        ("Pereira","Pereira"),
        ("Barranquilla", "Barranquilla"),
        ("Bucaramanga","Bucaramanga")
    ]

    city = forms.ChoiceField(label="city", choices=CITY_CHOICES)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')  # Assuming you have a password field in your form
        if password:
            user.set_password(password)  # Hash the password
        if commit:
            user.save()
        return user    
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if(len(password)<=6):
            raise forms.ValidationError("Contraseña: Contraseña muy corta, minimo 7 caracteres")
        elif(" " in password):
            raise forms.ValidationError("Contraseña: Espacios no permitidos")
        elif(password.lower()==password):
            raise forms.ValidationError("Contraseña: Minimo 1 caracter con mayusculas")
        elif(not(any(i.isdigit() for i in password))):
            raise forms.ValidationError("Contraseña: Minimo 1 numero")
            
        return password
      
class LoginForm(forms.ModelForm):

    def clean_email(self):
        email = forms.EmailField(required=True)
        return email
        

class CustomerChangeForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields =['email', 'password', 'first_name','last_name', 'address', 'city']
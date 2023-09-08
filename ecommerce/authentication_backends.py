from django.contrib.auth.backends import ModelBackend
from .models import CustomerUser

class EmailAuthBackend:
    
    def authenticate(self,request,username=None,password=None):
        try:
            user = CustomerUser.objects.get(email=username)
            print(user)
            if(user.check_password(password)):
                print("Good Password")
                return user
            return None
        except CustomerUser.DoesNotExist:
            print("Email failed")
            return None
        

        
    def get_user(self, user_id):
        try:
            return CustomerUser.objects.get(pk=user_id)
        except CustomerUser.DoesNotExist:
            print("Email failed, get_user")
            return None
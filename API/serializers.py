from rest_framework import serializers
from ecommerce import models

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    stock = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = ['id','name','stock','url']
    def get_url(self,obj):
        return f"http://127.0.0.1:8000/product/{obj.id}"
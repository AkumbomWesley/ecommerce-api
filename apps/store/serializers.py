from rest_framework import serializers
from apps.products.serializers import ProductSerializer
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'phone', 'email', 'products']


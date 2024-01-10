from rest_framework import serializers

from apps.products.serializers import ProductSerializer
from apps.users.models import User
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    class Meta:
        model = Store
        fields = ['owner', 'id', 'name', 'address', 'phone', 'email', 'products']


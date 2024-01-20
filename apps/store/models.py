from django.db import models
from apps.products.models import Product
from apps.users.models import User

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    products = models.ManyToManyField(Product, related_name='stores')
    owner = models.OneToOneField(User, on_delete = models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
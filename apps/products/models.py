from django.db import models
from apps.core.models import BaseModel

from apps import categories

class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
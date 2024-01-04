from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteAllView,
    ProductDeleteSingleView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='prdocuts-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/', ProductDeleteAllView.as_view(), name='product-delete-all'),
    path('<int:pk>/delete/', ProductDeleteSingleView.as_view(), name='product-delete-single'),
]
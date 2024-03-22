from django.urls import path
from .views import (
    StoreListView,
    StoreCreateView,
    StoreDeleteAllView,
    StoreDeleteSingleView,
    StoreDetailView,
    StoreUpdateView
)

urlpatterns = [
path('', StoreListView.as_view(), name='store-list'),
path('create-store/', StoreCreateView.as_view(), name='store-create'),
path('<int:pk>/detail/', StoreDetailView.as_view(), name='store-detail'),
path('<int:pk>/update/', StoreUpdateView.as_view(), name='store-update'),
path('<int:pk>/delete/', StoreDeleteSingleView.as_view(), name='store-delete'),
path('delete-all/', StoreDeleteAllView.as_view(), name='store-delete-all')
]
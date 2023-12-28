from django.urls import path
from .views import (
    UserCreateView,
    UserLoginView,
    GetUserView,
    UserUpdateView,
    GetAllUsersView,
    UserDeleteView,
    DeleteAllUsersView,
)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('<int:user_id>/', GetUserView.as_view(), name='get-user'),
    path('<int:user_id>/update/', UserUpdateView.as_view(), name='update-user'),
    path('', GetAllUsersView.as_view(), name='get-all-users'),
    path('<int:user_id>/delete/', UserDeleteView.as_view(), name='delete-user'),
    path('delete-all/', DeleteAllUsersView.as_view(), name='delete-all-users'),
]
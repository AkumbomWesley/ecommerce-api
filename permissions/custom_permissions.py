from rest_framework.permissions import BasePermission

#custom permission class 
class IsSuperUserOrAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin)

class IsStoreOwner(BasePermission):
    def has_permission(self, request, view):
           return request.user.is_authenticated and request.user.role == 'owner' and request.user.store_id is not None
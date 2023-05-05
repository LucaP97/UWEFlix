from rest_framework import permissions

class IsCinemaManagerOrAccountManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (hasattr(request.user, 'cinema_manager') or hasattr(request.user, 'accountmanager')))
    
class AccountManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'accountmanager'))
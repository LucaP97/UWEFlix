from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
class IsCinemaManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and hasattr(request.user, 'cinema_manager'))
    
class IsCinemaManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'cinema_manager'))

class IsStaffOrCinemaManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or hasattr(request.user, 'cinema_manager')))
    
class IsStudentOrStaffOrCinemaManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (hasattr(request.user, 'student') or request.user.is_staff or hasattr(request.user, 'cinema_manager')))
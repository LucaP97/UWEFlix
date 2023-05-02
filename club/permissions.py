from rest_framework import permissions

class IsCinemaManagerOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (hasattr(request.user, 'cinema_manager') or request.user.is_staff))
    
class IsCinemaManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and hasattr(request.user, 'cinema_manager'))
    
class IsCinemaManagerOrAccountManagerReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and hasattr(request.user, 'accountmanager'):
            return True
        return bool(request.user and hasattr(request.user, 'cinema_manager'))
    
class IsAccountManagerOrClubRepresentativeOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (hasattr(request.user, 'accountmanager') or hasattr(request.user, 'clubrepresentative')))

# class IsAccountManagerOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and hasattr(request.user, 'account_manager'))
    

# # club rep requires permission
# class IsClubRepresentativeOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and hasattr(request.user, 'club_representative'))
    

# class IsClubRepresentativeOrAccountManager(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if (bool(request.user and hasattr(request.user, 'clubrepresentative')) or bool(request.user and hasattr(request.user, 'account_manager'))) and request.method in permissions.SAFE_METHODS:
#             return True
#         elif request.method == 'PUT':
#             return bool(request.user and hasattr(request.user, 'clubrepresentative'))
#         return bool(request.user and hasattr(request.user, 'accountmanager'))


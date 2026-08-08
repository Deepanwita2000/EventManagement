# <<<<<<< HEAD
from rest_framework.permissions import BasePermission

# Permission to allow only admins to enroll
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin' 

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'organizer'

# Permission to allow only users to enroll
class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'

# User can be either a professor or a student
# This permission allows both professors and students to access the view
class IsOrganizerOrUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['organizer', 'user']
    
# class IsOrganizerOrUserOrAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role in ['organizer', 'user' , 'admin']
    


# class IsSuperuserOrOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Superuser can do anything
#         if request.user.is_superuser:
#             return True

#         # Organizer can only work on their own events
#         return obj.created_by == request.user
# =======
# from rest_framework.permissions import BasePermission

# # Permission to allow only admins to enroll
# # class IsAdmin(BasePermission):
# #     def has_permission(self, request, view):
# #         return request.user and request.user.is_authenticated and request.user.role == 'admin' 

# class IsOrganizer(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and request.user.role == 'organizer'

# # Permission to allow only users to enroll
# class IsUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'user'

# # User can be either a professor or a student
# # This permission allows both professors and students to access the view
# class IsOrganizerOrUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role in ['organizer', 'user']
    
# # class IsOrganizerOrUserOrAdmin(BasePermission):
# #     def has_permission(self, request, view):
# #         return request.user and request.user.role in ['organizer', 'user' , 'admin']
    
# >>>>>>> 3c71da83ca8249c58b92e6741917a4e4aada0e7c

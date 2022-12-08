from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        # Anyone can read
        # GET，HEAD, OPTIONS are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # only owner may write
        return obj.user == request.user

class IsUserMyself(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
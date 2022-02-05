from rest_framework import permissions


class IsGroupAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS: 
            if request.method == 'POST':
                return True
            else:
                return request.user == obj.admin
        return True

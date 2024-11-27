from django.core.exceptions import PermissionDenied

class IsStaffOrOwner:
    @staticmethod
    def has_permission(user, pk):
        if user.is_staff or user.has_perm('users.can_view_profile'):
            return True
        return False
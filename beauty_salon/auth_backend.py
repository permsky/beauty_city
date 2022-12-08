from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""
    def authenticate(self, phone_number=None):
        try:
            return CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

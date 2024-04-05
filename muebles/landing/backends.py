from django.contrib.auth.backends import BaseBackend
from .models import Usuario


class SettingsBackend(BaseBackend):

    def get_user(self, email):
        try:
            return Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return None

    def authenticate(self, email=None, password=None):

        user = self.get_user(email)
        if user is not None:
            if user.check_password(password):
                return user
        return None

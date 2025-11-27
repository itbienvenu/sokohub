
from django.contrib.auth.backends import BaseBackend
from Account.models import Account

class AccountBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return None
        
        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None

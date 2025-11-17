from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Account

class AccountBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return None

        if check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None

# """
# {
# "password":"tyuio",
# "email":mmmm,
# }
# """

# [
#     {"email":"tghujikl","passs":"rt6y78i9o0p"},
#     {"email":"t6y7u8i9","pass":"567890-"}
# ]

# val = {"email":"tghujikl","passs":"rt6y78i9o0p"}

# print(val["email"])
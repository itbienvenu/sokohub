from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated:
            if user.user_type == 'vendor':
                return resolve_url('vendor_dashboard')
            else:
                return resolve_url('product_list')
        return resolve_url(settings.LOGIN_REDIRECT_URL)

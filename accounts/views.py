from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, LoginForm
from .models import User, PasswordResetOTP
import random
from .methods import send_email


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            otp_hash = hash(otp)
            PasswordResetOTP.objects.create(user=user, otp_hash=otp_hash)
            send_email(user.email, 'Password Reset OTP', f'Your OTP is: {otp}')
            redirect('password_reset_confirm')

    return render(request, 'accounts/reset_password.html')




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.user_type == 'vendor':
                return redirect('vendor_dashboard')
            else:
                return redirect('product_list')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    
    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'vendor':
            return '/vendor/dashboard/'
        else:
            return '/products/'

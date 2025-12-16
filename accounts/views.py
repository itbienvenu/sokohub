from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, LoginForm
from .models import User, PasswordResetOTP
import random
from .methods import send_email
from datetime import timedelta, UTC, datetime
from django.utils import timezone
from django.contrib import messages
import hashlib


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            otp_hash = hashlib.sha256(otp.encode()).hexdigest()
            # Invalidate/delete old OTPs for this user to prevent clutter and confusion
            PasswordResetOTP.objects.filter(user=user).delete()
            PasswordResetOTP.objects.create(user=user, otp_hash=otp_hash)
            
            send_email(user.email, 'Password Reset OTP', f'Your OTP is: {otp}')
            request.session['reset_email'] = email
            messages.success(request, f'OTP sent to {email}. Please check your inbox.')
            return redirect('verify_otp')
        else:
            messages.error(request, 'User with this email does not best exist.')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


def verify_otp(request):
    current_time = timezone.now() 
    email = request.session.get('reset_email')
    
    if not email:
        messages.error(request, 'Session expired. Please start the password reset process again.')
        return redirect('reset_password')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        submitted_otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        try:
            # Verify OTP for the specific user in session
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp_hash=submitted_otp_hash).first()
            
            if not otp_obj:
                 raise PasswordResetOTP.DoesNotExist
                 
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            messages.error(request, 'Invalid code. Please try again.')
            return redirect('verify_otp')

        expiry_time = otp_obj.created_at + timedelta(minutes=5)

        if expiry_time < current_time:
            otp_obj.delete()
            messages.error(request, 'Verification code has expired. Please request a new one.')
            return redirect('reset_password')
        
        user_id = otp_obj.user.pk
        
        # Clear sensitive session data as we move to token-based URL
        # But keeping it might be useful if we wanted to verify user in next step too.
        # For now, following original flow:
        return redirect('set_new_password', user_id=user_id, token=submitted_otp_hash)

    return render(request, 'accounts/reset_password_confirm.html')


def set_new_password(request, user_id, token):
    try:
        otp_obj = PasswordResetOTP.objects.get(user__pk=user_id, otp_hash=token)
    except PasswordResetOTP.DoesNotExist:
        messages.error(request, 'Invalid or expired link.')
        return redirect('reset_password')

    current_time = timezone.now()
    expiry_time = otp_obj.created_at + timedelta(minutes=5)

    if expiry_time < current_time:
        otp_obj.delete()
        messages.error(request, 'Verification link has expired. Please request a new one.')
        return redirect('reset_password')

    user = otp_obj.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            otp_obj.delete()
            if 'reset_email' in request.session:
                del request.session['reset_email']
            messages.success(request, 'Password changed successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            
    context = {'user_id': user_id, 'token': token}
    return render(request, 'accounts/set_new_password.html', context)




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

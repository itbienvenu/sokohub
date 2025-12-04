from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, LoginForm

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

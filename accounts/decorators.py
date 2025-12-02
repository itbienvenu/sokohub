from django.contrib.auth.decorators import user_passes_test

def vendor_required(function=None, redirect_field_name='next', login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 'vendor',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def customer_required(function=None, redirect_field_name='next', login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == 'customer',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

from django.shortcuts import render
from .models import Account


# Create your views here.

def accounts_list(request):

    all_accounts = Account.objects.all().order_by('names')

    context = {
        'accounts': all_accounts
    }

    return render(request, 'account/test.html', context)

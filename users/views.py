from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

from mainApp.utils import generate_btc

from .forms import UserRegisterForm
from mainApp.models import Wallet


@login_required
def home(request):
    return render(request, 'users/home.html')


def register(request):
    # GET we disply the form
    # POST we save the data

    context = {}
    print(request.method)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # flash message
      
            user = form.save()
            btc_balance = generate_btc()
            wallet = Wallet.objects.create(user = user, btc_balance = btc_balance)
            wallet.save()
            messages.success(request, f"Your account has been created with {btc_balance} bitcoins ! You are now able to log in")

            return redirect('login')

    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

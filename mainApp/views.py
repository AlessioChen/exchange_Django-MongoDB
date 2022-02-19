from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mainApp.forms import OrderCreationForm
from mainApp.models import Order, Wallet

@login_required
def home(request):

    context = {
        'orders': Order.objects.filter(user = request.user),
        'balance':  getUserBalance(request.user)
        
    }

    return render(request, 'users/home.html', context)

@login_required
def sell(request):
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST) 
        if form.is_valid(): 
            user_wallet = Wallet.objects.filter(user = request.user).first()
            btc_quantity = form.cleaned_data['btc_quantity']
            if not canSell(user_wallet, btc_quantity ):
               messages.error(request, 'You do not have enouth BTC to sell ')
               return redirect('home')
            
            order = form.save()
            order.user = request.user
            order.type="sell"
            order.order_status = "pending"
            order.save()

            user_wallet.btc_balance -= btc_quantity
            user_wallet.save()
            messages.success(request, 'Your sell order has been placed!')
            return redirect('home')

    context = {
        'form': form, 
        'orders': Order.objects.filter(user = request.user), 
        'balance': getUserBalance(request.user)
    }
   
    return render(request, 'mainApp/order.html', context)

@login_required
def buy(request):
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST) 
        if form.is_valid(): 
            user_wallet = Wallet.objects.filter(user = request.user).first()
            price = form.cleaned_data['price']
            if not canBuy(user_wallet, price ):
               messages.error(request, 'You do not have enouth $ to buy ')
               return redirect('home')
            
            order = form.save()
            order.user = request.user
            order.type="buy"
            order.order_status = "pending"
            order.save()

            user_wallet.money_balance -= price
            user_wallet.save()
            messages.success(request, 'Your buy order has been placed!')
            return redirect('home')

    context = {
        'form': form, 
        'orders': Order.objects.filter(user = request.user), 
        'balance': getUserBalance(request.user)
    }
   
    return render(request, 'mainApp/order.html', context)



def getUserBalance(user):
    balance = {
        'btc': Wallet.objects.filter(user = user).first().btc_balance, 
        'money': Wallet.objects.filter(user = user).first().money_balance
    }

    return balance

def canSell(user_wallet, btc_quantity):
    if(user_wallet.btc_balance < btc_quantity):
        return False 

    return True 

def canBuy(user_wallet, price):
    if(user_wallet.money_balance < price):
        return False 

    return True 
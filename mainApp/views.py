from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mainApp.forms import OrderCreationForm
from mainApp.models import Order, Transaction, Wallet


@login_required
def home(request):

    context = {
        'sell_orders': Order.objects.filter(user=request.user, type="sell", order_status="pending"),
        'balance':  getUserBalance(request.user),
        'buy_orders': Order.objects.exclude(user=request.user).filter(type="sell", order_status="pending"),
    }

    return render(request, 'users/home.html', context)


@login_required
def sell(request):
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            btc_quantity = form.cleaned_data['btc_quantity']
            if not canSell(user_wallet, btc_quantity):
                messages.error(request, 'You do not have enouth BTC to sell ')
                return redirect('home')

            order = form.save()
            order.user = request.user
            order.type = "sell"
            order.order_status = "pending"
            order.save()

            user_wallet.btc_balance -= btc_quantity
            user_wallet.save()
            messages.success(request, 'Your sell order has been placed!')
            return redirect('home')

    context = {
        'form': form,
        'orders': Order.objects.filter(user=request.user),
        'balance': getUserBalance(request.user)
    }

    return render(request, 'mainApp/order.html', context)


def delete_order (request, pk):

    order = getOrder(pk)
    user = order.user 
    wallet = Wallet.objects.filter(user = user).first()
    wallet.btc_balance += order.btc_quantity
    wallet.save()
    refund_btc = order.btc_quantity
    order.delete()
    messages.success(request, f"Your sell order has been cancelled and we have refunded you {refund_btc} BTC")
   

    return redirect('home')

@login_required
def buy_btc(request, pk):

    order = getOrder(pk)
    buyer = request.user 
    buyer_wallet = Wallet.objects.filter(user= buyer).first()
    seller = order.user
    seller_wallet = Wallet.objects.filter(user = seller).first()

    if not canBuy(buyer_wallet, order.price):
        messages.error(request, 'You do not have enouth $ to buy ')
        return redirect('home')

    transaction(buyer_wallet, seller_wallet, order  )
    messages.success(request, "Your order has been placed successfully")
    return redirect('home')


def getUserBalance(user):
    balance = {
        'btc': Wallet.objects.filter(user=user).first().btc_balance,
        'money': Wallet.objects.filter(user=user).first().money_balance
    }

    return balance

def getOrder(pk):
    for order in Order.objects.all(): 
        if(str(order.pk) == pk): 
            return order

def canSell(user_wallet, btc_quantity):
    if(user_wallet.btc_balance < btc_quantity):
        return False

    return True


def canBuy(user_wallet, price):
    if(user_wallet.money_balance < price):
        return False

    return True


def transaction(buyer_wallet, seller_wallet, order):
    buyer_wallet.btc_balance += order.btc_quantity
    seller_wallet.money_balance += order.price 

    order.order_status = 'completed'
    buyer_wallet.save()
    seller_wallet.save()
    order.save()

    transaction = Transaction(buyer = buyer_wallet.user, 
                              seller = seller_wallet.user,
                              btc_quantity = order.btc_quantity, 
                              price = order.price,
                              datetime = datetime.now() ) 

    transaction.save()
 

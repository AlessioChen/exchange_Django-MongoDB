from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mainApp.forms import OrderCreationForm
from mainApp.models import Order, Wallet
from .utils import *


@login_required
def home(request):

    context = {
        "open_orders": Order.objects.filter(user=request.user, order_status="pending"),
        "balance": getUserBalance(request.user),
        "marker_orders": Order.objects.exclude(user=request.user).filter(
            order_status="pending"
        ),
    }

    return render(request, "users/home.html", context)


@login_required
def sell(request):
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            btc_quantity = form.cleaned_data["btc_quantity"]

            if not canSell(user_wallet, btc_quantity):
                messages.error(request, "You do not have enouth BTC to sell ")
                return redirect("home")

            order = form.save()
            order.user = request.user
            order.type = "sell"
            order.order_status = "pending"
            order.save()

            match_sell_order(order)

            messages.success(request, "Your sell order has been placed!")

            return redirect("home")

    context = {
        "form": form,
        "orders": Order.objects.filter(user=request.user),
        "balance": getUserBalance(request.user),
    }

    return render(request, "mainApp/order.html", context)


@login_required
def buy(request):
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            price = form.cleaned_data["price"]
            btc_quantity = form.cleaned_data["btc_quantity"]
            if not canBuy(user_wallet, price, btc_quantity):
                messages.error(request, "You do not have enouth $ to buy ")
                return redirect("home")

            order = form.save()
            order.user = request.user
            order.type = "buy"
            order.order_status = "pending"
            order.save()

            # user_wallet.money_balance -= price
            # user_wallet.save()
            messages.success(request, "Your buy order has been placed!")
            return redirect("home")

    context = {
        "form": form,
        "orders": Order.objects.filter(user=request.user),
        "balance": getUserBalance(request.user),
    }

    return render(request, "mainApp/order.html", context)


@login_required
def delete_order(request, pk):

    order = getOrder(pk)
    order.delete()
    messages.success(
        request,
        f"Your sell order has been cancelled",
    )

    return redirect("home")


@login_required
def open_orders(request):
    open_order = []
    for order in Order.objects.filter(order_status="pending"):
        open_order.append(
            {
                "id": str(order.pk),
                "user": str(order.user),
                "type": order.type,
                "order_status": order.order_status,
                "price": order.price,
                "btc_quantity": order.btc_quantity,
            }
        )

    res = {"orders ": open_order}
    return JsonResponse(res)


@login_required
def profit_all_users(request):

    profits = {}
    for user in User.objects.all():
        item = {user.username: {"btc_profit": 0, "money_profit": 0}}
        profits.update(item)

    for transaction in Transaction.objects.all():
        buyer = transaction.buyer.username
        seller = transaction.seller.username

        profits[buyer]["btc_profit"] += transaction.btc_quantity
        profits[buyer]["money_profit"] -= transaction.price * transaction.btc_quantity

        profits[seller]["btc_profit"] -= transaction.btc_quantity
        profits[seller]["money_profit"] += transaction.price * transaction.btc_quantity

    return JsonResponse(profits)

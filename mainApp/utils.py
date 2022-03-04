from distutils.log import WARN
import random
from tkinter import W
from mainApp.models import Order, Transaction, Wallet
from datetime import datetime


def generate_random_number(max_value):
    return random.uniform(1, max_value)


def getUserBalance(user):
    balance = {
        "btc": Wallet.objects.filter(user=user).first().btc_balance,
        "money": Wallet.objects.filter(user=user).first().money_balance,
    }

    return balance


def getOrder(pk):
    for order in Order.objects.all():
        if str(order.pk) == pk:
            return order


def canSell(user_wallet, btc_quantity):
    if user_wallet.btc_balance < btc_quantity:
        return False

    return True


def canBuy(user_wallet, price, btc_quanty):
    if user_wallet.money_balance < price * btc_quanty:
        return False

    return True


def match_sell_order(sell_order):

    buy_orders = (
        Order.objects.order_by("-modified")
        .filter(type="buy", order_status="pending")
        .exclude(user=sell_order.user)
    )

    for buy_order in buy_orders:
        if sell_order.order_status == "completed":
            continue

        if buy_order.btc_quantity == sell_order.btc_quantity:
            sell_order.price = buy_order.price
            sell_order.order_status = "completed"
            buy_order.order_status = "completed"
            sell_transaction(sell_order, buy_order)

        elif buy_order.btc_quantity > sell_order.btc_quantity:
            sell_order.price = buy_order.price
            sell_order.order_status = "completed"
            buy_order.btc_quantity -= sell_order.btc_quantity
            if buy_order.btc_quantity == 0:
                buy_order.order_status = "completed"
            sell_transaction(sell_order, buy_order)

        elif buy_order.btc_quantity < sell_order.btc_quantity:
            sell_order.btc_quantity -= buy_order.btc_quantity

            if sell_order.btc_quantity == 0:
                sell_order.order_status = "completed"
            buy_order.order_status = "completed"

            sell_transaction(sell_order, buy_order)

        sell_order.save()
        buy_order.save()


def sell_transaction(sell_order, buy_order):
    seller_wallet = Wallet.objects.filter(user=sell_order.user).first()
    buyer_wallet = Wallet.objects.filter(user=buy_order.user).first()

    if buy_order.btc_quantity == sell_order.btc_quantity:
        seller_wallet.money_balance += sell_order.price * sell_order.btc_quantity

        buyer_wallet.btc_balance += sell_order.btc_quantity
        buyer_wallet.money_balance -= buy_order.price * buy_order.btc_quantity
    elif buy_order.btc_quantity > sell_order.btc_quantity:
        seller_wallet.money_balance += sell_order.price * sell_order.btc_quantity

        buyer_wallet.btc_balance += sell_order.btc_quantity
        buyer_wallet.btc_balance -= buy_order.price * sell_order.btc_quantity
    elif buy_order.btc_quantity < sell_order.btc_quantity:
        seller_wallet.money_balance += buy_order.price * buy_order.btc_quantity

        buyer_wallet.money_balance -= buy_order.price * buy_order.btc_quantity
        buyer_wallet.btc_balance += buy_order.btc_quantity

    seller_wallet.save()
    buyer_wallet.save()

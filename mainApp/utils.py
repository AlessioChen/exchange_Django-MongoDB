import random
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


def canBuy(user_wallet, price):
    if user_wallet.money_balance < price:
        return False

    return True


def transaction(buyer_wallet, seller_wallet, order):
    buyer_wallet.btc_balance += order.btc_quantity
    seller_wallet.money_balance += order.price

    order.order_status = "completed"
    buyer_wallet.save()
    seller_wallet.save()
    order.save()

    transaction = Transaction(
        buyer=buyer_wallet.user,
        seller=seller_wallet.user,
        btc_quantity=order.btc_quantity,
        price=order.price,
        datetime=datetime.now(),
    )

    transaction.save()

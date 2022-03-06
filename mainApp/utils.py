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


def canBuy(user_wallet, price, btc_quanty):
    if user_wallet.money_balance < price * btc_quanty:
        return False

    return True


def update_orders(sell_order, buy_order):
    # full fill sell and buy
    if sell_order.btc_quantity == buy_order.btc_quantity:
        sell_order.order_status = "completed"
        buy_order.order_status = "completed"

    # full fill sell and partially fill buy
    elif sell_order.btc_quantity > buy_order.btc_quantity:
        sell_order.btc_quantity -= buy_order.btc_quantity
        buy_order.order_status = "completed"

        # full fill buy and partally fill sell
    elif sell_order.btc_quantity < buy_order.btc_quantity:
        buy_order.btc_quantity -= sell_order.btc_quantity
        sell_order.order_status = "completed"

    sell_order.save()
    buy_order.save()


def transaction(sell_order, buy_order):
    seller_wallet = Wallet.objects.filter(user=sell_order.user).first()
    buyer_wallet = Wallet.objects.filter(user=buy_order.user).first()
    # save transaction
    transaction = Transaction(
        buyer=buyer_wallet.user,
        seller=seller_wallet.user,
        btc_quantity=buy_order.btc_quantity,
        price=buy_order.price,
        datetime=datetime.now(),
    )

    transaction.save()


def match_buy_order(buy_order):
    sell_orders_list = (
        Order.objects.filter(
            type="sell", order_status="pending", price__lte=buy_order.price
        )
        .exclude(user=buy_order.user)
        .order_by("price")
    )

    for sell_order in sell_orders_list:

        seller_wallet = Wallet.objects.filter(user=sell_order.user).first()
        buyer_wallet = Wallet.objects.filter(user=buy_order.user).first()

        buy_order.price = sell_order.price
        buy_order.save()

        update_orders(sell_order, buy_order)

        seller_wallet.btc_balance -= sell_order.btc_quantity
        seller_wallet.money_balance += sell_order.btc_quantity * sell_order.price
        seller_wallet.save()

        buyer_wallet.btc_balance += sell_order.btc_quantity
        buyer_wallet.money_balance -= sell_order.btc_quantity * sell_order.price
        buyer_wallet.save()

        transaction(sell_order, buy_order)


def match_sell_order(sell_order):

    buy_orders_list = (
        Order.objects.filter(
            type="buy", order_status="pending", price__gte=sell_order.price
        )
        .exclude(user=sell_order.user)
        .order_by("-price")
    )

    for buy_order in buy_orders_list:

        seller_wallet = Wallet.objects.filter(user=sell_order.user).first()
        buyer_wallet = Wallet.objects.filter(user=buy_order.user).first()

        sell_order.price = buy_order.price
        sell_order.save()

        update_orders(sell_order, buy_order)

        seller_wallet.btc_balance -= buy_order.btc_quantity
        seller_wallet.money_balance += buy_order.btc_quantity * buy_order.price
        seller_wallet.save()

        buyer_wallet.btc_balance += buy_order.btc_quantity
        buyer_wallet.money_balance -= buy_order.btc_quantity * buy_order.price
        buyer_wallet.save()

        transaction(sell_order, buy_order)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sell_btc", views.sell, name="sell"),
    path("buy_btc", views.buy, name="buy"),
    path("buy_btc/<str:pk>", views.buy_btc, name="buy_btc"),
    path("delete_order/<str:pk>", views.delete_order, name="delete_order"),
    path("open_orders", views.open_orders, name="open_orders"),
    path("profit_all_users", views.profit_all_users, name="profit_all_users"),
]

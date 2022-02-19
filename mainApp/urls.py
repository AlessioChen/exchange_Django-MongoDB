from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sell_btc', views.sell, name="sell"),
    path('buy_btc', views.buy, name="buy")
]

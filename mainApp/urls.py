from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sell_btc', views.sell, name="sell"),
    path('buy_btc/<str:pk>', views.buy_btc, name="buy_btc"), 
    path('delete_order/<str:pk>', views.delete_order, name="delete_order"), 
    path("open_orders", views.open_orders, name="open_orders")
]

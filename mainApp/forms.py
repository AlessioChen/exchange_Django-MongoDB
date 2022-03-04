from .models import Order
from django import forms


class OrderCreationForm(forms.ModelForm):
    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Price can not be negative")
        return price

    def clean_btc_quantity(self):
        btc_quanty = self.cleaned_data["btc_quantity"]
        if btc_quanty < 0:
            raise forms.ValidationError("BTC quantity can not be negative")
        return btc_quanty

    class Meta:
        model = Order
        fields = ("price", "btc_quantity")

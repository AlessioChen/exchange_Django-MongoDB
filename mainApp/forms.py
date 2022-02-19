from .models import Order
from django import forms

class OrderCreationForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ('price' , 'btc_quantity')
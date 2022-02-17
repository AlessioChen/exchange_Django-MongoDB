from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

#djongo
from djongo.models.fields import ObjectIdField
from djongo import models

class Wallet(models.Model):
  _id = ObjectIdField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  btc_balance = models.FloatField()
  money_balance = models.FloatField()

  def save(self, *args, **kwargs):
      self.money_balance = round(self.money_balance, 2)
      super(Wallet, self).save(*args, **kwargs)

class Order(models.Model):
  _id= ObjectIdField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  type = models.CharField(max_length=4, choices= (('buy', 'buy'), ('sell', 'sell')))
  order_status = models.CharField(max_length=10, choices=(('pending', 'pending'), ('completed', 'completed')))
  price = models.FloatField()
  btc_quantity = models.FloatField()

class Trade(models.Model):
  _id = ObjectIdField()
  buyer_user = models.ForeignKey(User, related_name='buyer',on_delete=models.CASCADE)
  seller_user = models.ForeignKey(User, related_name='seller',on_delete=models.CASCADE)
  btc_quantity = models.FloatField()
  price = models.FloatField()
  datetime = models.DateTimeField(auto_now_add=True)
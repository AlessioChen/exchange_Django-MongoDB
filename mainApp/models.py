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
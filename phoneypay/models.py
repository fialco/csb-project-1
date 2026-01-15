from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField()
    balance = models.IntegerField()

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField()
    balance = models.IntegerField()


class Transaction(models.Model):
    from_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="outgoing_transaction"
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="incoming_transaction"
    )
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

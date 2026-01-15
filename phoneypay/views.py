from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from .models import Account


@transaction.atomic
def transfer(sender, receiver, amount):
    acc1 = Account.objects.get(id=sender)
    acc2 = Account.objects.get(id=receiver)

    if amount < 1 or acc1 == acc2:
        return

    if acc1.balance - amount < 0:
        return

    acc1.balance -= amount
    acc2.balance += amount

    acc1.save()
    acc2.save()


@login_required
def sendView(request):
    sender = Account.objects.get(owner__username=request.user)
    receiver = int(request.POST.get("receiver"))
    amount = int(request.POST.get("amount"))

    transfer(sender.id, receiver, amount)

    return redirect("/")


@login_required
def index(request):
    account = Account.objects.get(owner__username=request.user)
    numbers = Account.objects.filter(~Q(phone=account.phone))
    return render(request, "pages/index.html", {"account": account, "numbers": numbers})

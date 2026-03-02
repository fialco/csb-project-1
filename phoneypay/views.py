from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.db import transaction
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction


# Flaw 1 fix: add check for proper authentication
# @staff_member_required
def statistics_view(request):
    total_users = Account.objects.count()

    transfer_stats = Transaction.objects.aggregate(
        total_transfers=Count("id"),
        total_amount=Sum("amount", default=0),
    )

    statistics = {
        "total_users": total_users,
        "total_transfers": transfer_stats["total_transfers"],
        "total_amount": transfer_stats["total_amount"],
    }
    return render(request, "pages/statistics.html", {"statistics": statistics})


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

    Transaction.objects.create(from_account=acc1, to_account=acc2, amount=amount)


@login_required
# Flaw 2 fix: remove @csrf_exempt and add {% csrf_token %} in index.html
@csrf_exempt
def send_view(request):
    sender = Account.objects.get(owner__username=request.user)
    receiver = int(request.POST.get("receiver"))
    amount = int(request.POST.get("amount"))
    transfer(sender.id, receiver, amount)

    return redirect("/")


@login_required
def search_view(request):
    account = Account.objects.get(owner__username=request.user)
    phone = request.GET.get("phone", "")

    # FLAW 3: A03:2021 – Injection
    query = f"""SELECT t.*
FROM phoneypay_transaction t
INNER JOIN phoneypay_account fa
    ON t.from_account_id = fa.id
INNER JOIN phoneypay_account ta
    ON t.to_account_id = ta.id
WHERE
    (
        t.from_account_id = '{account.id}'
        AND ta.phone = '{phone}'
    )
    OR
    (
        t.to_account_id = '{account.id}'
        AND fa.phone = '{phone}'
    )"""
    results = Transaction.objects.raw(query)

    # Flaw 3 fix version 1: switch to parameters
    #
    # query = f"""SELECT t.*
    # FROM phoneypay_transaction t
    # INNER JOIN phoneypay_account fa
    #    ON t.from_account_id = fa.id
    # INNER JOIN phoneypay_account ta
    #    ON t.to_account_id = ta.id
    # WHERE
    #    (
    #        t.from_account_id = %s
    #        AND ta.phone = %s
    #    )
    #    OR
    #    (
    #        t.to_account_id = %s
    #        AND fa.phone = %s
    #    )"""
    #    results = Transaction.objects.raw(query, [account.id, phone, account.id, phone])

    # Flaw 3 fix version 2: use Django ORM query
    """
    results = Transaction.objects.select_related("from_account", "to_account").filter(
        Q(from_account_id=account.id, to_account__phone=phone)
        | Q(to_account_id=account.id, from_account__phone=phone)
    ).order_by("timestamp")

    """
    return render(
        request, "pages/search.html", {"account": account, "results": results}
    )


@login_required
def index(request):
    account = Account.objects.get(owner__username=request.user)
    numbers = Account.objects.filter(~Q(phone=account.phone))

    transactions = (
        Transaction.objects.select_related("from_account", "to_account")
        .filter(Q(from_account_id=account.id) | Q(to_account=account.id))
        .order_by("timestamp")
    )

    return render(
        request,
        "pages/index.html",
        {
            "account": account,
            "numbers": numbers,
            "transactions": transactions,
        },
    )

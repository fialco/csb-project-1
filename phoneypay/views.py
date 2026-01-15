from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Account


@login_required
def index(request):
    account = Account.objects.get(owner__username=request.user)
    numbers = Account.objects.filter(~Q(phone=account.phone))
    return render(request, "pages/index.html", {"account": account, "numbers": numbers})

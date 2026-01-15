from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Account


@login_required
def index(request):
    account = Account.objects.get(owner__username=request.user)
    return render(request, "pages/index.html", {"account": account})

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account, Message
from django.db.models import Q

@login_required
def transferView(request):
    #this whole part of the function should be removed/commented out and the one below it uncommented to fix flaw #3, the index.html also has a few things to change
    
    request.session['to'] = request.GET.get('to')
    request.session['amount'] = int(request.GET.get('amount'))
    amount= request.session['amount']
    receiver=User.objects.get(username=request.session['to'])
    sender_account=Account.objects.get(user=request.user)
    receiving_account=Account.objects.get(user=receiver)
    with transaction.atomic():
        if sender_account.balance < amount:
            return redirect('/')
        sender_account.balance -= amount
        sender_account.save()
        receiving_account.balance += amount
        receiving_account.save()
    """ #Fix for flaw #3, switching to POST instead of GET (additionally requires fixing the html component )
    if request.method == 'POST':
        to_username = request.POST.get('to')
        amount = int(request.POST.get('amount', 0))
        recipient = User.objects.get(username=to_username)
        if recipient == request.user or amount <=0:
            return redirect('/')
        sender_account = Account.objects.get(user=request.user)
        receiving_account = Account.objects.get(user=recipient)
        with transaction.atomic():
            if sender_account.balance < amount:
                return redirect('/')
            sender_account.balance -= amount
            sender_account.save()
            receiving_account.balance += amount
            receiving_account.save()
            print("transaction successful, this message is for testing/project screenshots")
    else:
        print("transaction unsuccessful, this message is for testing/project screenshots")
    """
    return redirect('/')

@login_required
def addView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
	return redirect('/')


@login_required
def homePageView(request):
    messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user))
    accounts = Account.objects.exclude(user_id=request.user.id)
    return render(request, 'pages/index.html', {'accounts': accounts, 'messages':messages})
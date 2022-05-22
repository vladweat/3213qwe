from unittest import result
from django.shortcuts import redirect, render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from .forms import ProposalCreationForm
from .models import Proposal

from web3 import Web3, HTTPProvider, eth, Account
from dotenv import dotenv_values

config = dotenv_values(".env")

# bank address
bank_address = config.get("BANK_ADDRESS")
bank_private_key = config.get("BANK_PRIVATE_KEY")

@login_required
def view_proposal(request):
    return HttpResponse("view_proposal")

@login_required
def creating_proposal(request):
    balance = get_balance(request)
    data = Proposal.objects.all()
    
    if request.method == "POST":
        
        form = ProposalCreationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            
            cd = form.cleaned_data
            
            proposal = Proposal()
            proposal.long_name = cd["long_name"]
            proposal.short_name = cd["short_name"]
            proposal.description = cd["description"]
            
            proposal.creator = request.user
            proposal.set_status(0)
            
            print(cd)
            
            proposal.save()
            
            data = proposal.long_name
            
            return render(
                request,
                "web3app/creating_proposal.html",
                {"balance": balance, "data": data, "form": form},
            )
        else:
            print("form is not valid")
            return render(
                request,
                "web3app/creating_proposal.html",
                {"balance": balance, "data": data, "form": form},
            )
    else:
        form = ProposalCreationForm()
        
    return render(
        request,
        "web3app/creating_proposal.html",
        {"balance": balance, "data": data, "form": form},
    )


def get_balance(request):
    web3 = Web3(
        HTTPProvider("https://rinkeby.infura.io/v3/32a867e993e44d8bbd973382f147e060")
    )
    raw_balance = web3.eth.get_balance(request.user.eth_address)
    balance = web3.fromWei(raw_balance, "ether")
    # check = web3.isConnected()
    # result = f"User {request.user.eth_address} is trying connect to web3, answer - {check}"
    # result = f"Balance of {request.user.eth_address} - {balance}"
    return balance


# @login_required
# def forma(request):
#     data = "rundom hueta"
#     return creating_proposal(request, input_data=data)

# @login_required
# def cr_proposal(request):
#     if request.method == "POST":
#         form = ProposalCreationForm(request.POST)
#         data = {}

#         if form.is_valid():

#             return creating_proposal(request, data=data, form=form)
#     else:
#         return HttpResponseRedirect("creating_proposal")


####################################################################################

# неактуально <form action="{% url 'check_web3' %}" method="post">
@login_required
def check_web3(request):
    if request.method == "POST":
        # print(send_from_bank_to_account(request))
        return creating_proposal(request)
    else:
        return HttpResponseRedirect("creating_proposal")

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

from web3 import Web3, HTTPProvider


def creating_proposal(request):
    return render(request, "web3app/creating_proposal.html")

def connect_to_web3(request):
    web3 = Web3(
            HTTPProvider(
                "https://rinkeby.infura.io/v3/32a867e993e44d8bbd973382f147e060"
            )
        )
    check = web3.isConnected()
    result = f"User {request.user.eth_address} is trying connect to web3, answer - {check}" 
    return result


@login_required
def check_web3(request):
    if request.method == "POST":
        print(connect_to_web3(request))
        return HttpResponsePermanentRedirect("/creating_proposal")
    else:
        return HttpResponseRedirect("creating_proposal")
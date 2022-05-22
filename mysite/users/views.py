from django.shortcuts import redirect, render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from eth_account import Account
import secrets

from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, LoginForm

from web3 import Web3, HTTPProvider

bank_address = "0xB5dea2661dfa4b8f0aaE8Bc1F583369D927c3b06"
bank_private_key = "0xcad32d1bbf83420e30b80cbe1f944dfe510db0af34ab42f0341b67f5f7da530a"

# Create your views here.
def index(request):
    if request.method == "POST":
        return HttpResponsePermanentRedirect("/login")
    else:
        return render(request, "index.html")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect("/creating_proposal")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "users/login_page.html", {"form": form})


@login_required
def check_web3(request):
    if request.method == "POST":
        web3 = Web3(
            HTTPProvider(
                "https://rinkeby.infura.io/v3/32a867e993e44d8bbd973382f147e060"
            )
        )
        res = web3.isConnected()
        print(res)
        redirect("creating_proposal")
    else:
        return HttpResponseRedirect("creating_proposal")


@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/login")

def send_from_bank_to_account(user):
    web3 = Web3(
        HTTPProvider("https://rinkeby.infura.io/v3/32a867e993e44d8bbd973382f147e060")
    )
    nonce = web3.eth.getTransactionCount(bank_address)
    
    tx = {
        "nonce": nonce,
        "to": user.eth_address,
        "value": web3.toWei(0.005, "ether"),
        "gas": 2000000,
        "gasPrice": web3.toWei('50', 'gwei')
    }
    
    signed_tx = web3.eth.account.sign_transaction(tx, bank_private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


def registr(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # private_key creating and ETH address
            private_phase = secrets.token_hex(32)
            private_key = "0x" + private_phase
            account = Account.from_key(private_key)

            new_user.private_key = private_key
            new_user.eth_address = account.address

            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save(update_fields=["private_key", "eth_address"])
            
            send_from_bank_to_account(new_user)
            
            return HttpResponsePermanentRedirect("/login")
            # return render(request, "users/login_page.html", {"new_user": new_user})
    else:
        user_form = CustomUserCreationForm()
    return render(request, "users/registr_page.html", {"user_form": user_form})

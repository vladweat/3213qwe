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

from web3 import Web3, HTTPProvider, eth, Account


bank_address = "0xB5dea2661dfa4b8f0aaE8Bc1F583369D927c3b06"
bank_private_key = "0xcad32d1bbf83420e30b80cbe1f944dfe510db0af34ab42f0341b67f5f7da530a"


def creating_proposal(request):
    balance = connect_to_web3(request)
    # tx_hash = send_from_bank_to_account(request)
    return render(request, "web3app/creating_proposal.html", {"balance": balance})


def connect_to_web3(request):
    web3 = Web3(
        HTTPProvider("https://rinkeby.infura.io/v3/32a867e993e44d8bbd973382f147e060")
    )
    raw_balance = web3.eth.get_balance(request.user.eth_address)
    balance = web3.fromWei(raw_balance, "ether")
    # check = web3.isConnected()
    # result = f"User {request.user.eth_address} is trying connect to web3, answer - {check}"
    # result = f"Balance of {request.user.eth_address} - {balance}"
    return balance

def send_from_bank_to_account(request):
    web3 = Web3(
        HTTPProvider("https://rinkeby.infura.io/v3/32a867e993e44d8bbd973382f147e060")
    )
    nonce = web3.eth.getTransactionCount(bank_address)
    
    tx = {
        "nonce": nonce,
        "to": request.user.eth_address,
        "value": web3.toWei(0.005, "ether"),
        "gas": 2000000,
        "gasPrice": web3.toWei('50', 'gwei')
    }
    
    signed_tx = web3.eth.account.sign_transaction(tx, bank_private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)
    
@login_required
def check_web3(request):
    if request.method == "POST":
        # print(send_from_bank_to_account(request))
        return HttpResponsePermanentRedirect("/creating_proposal")
    else:
        return HttpResponseRedirect("creating_proposal")

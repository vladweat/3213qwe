import json
import os

from django.shortcuts import redirect, render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import ProposalCreationForm
from .models import Proposal

# web3
from web3 import Web3, HTTPProvider, eth, Account
from dotenv import dotenv_values

# brownie
from brownie.build.contracts import *

config = dotenv_values(".env")

# bank address
bank_address = config.get("BANK_ADDRESS")
bank_private_key = config.get("BANK_PRIVATE_KEY")
infura_url = config.get("INFURA_URL")
contract_address = config.get("CONTRACT_ADDRESS")

# old version
# def connect_to_smart_contract(request):
#     # import deploying contract json file from brownie
#     with open(
#         os.path.join(settings.BASE_DIR, "brownie/build/contracts/SimpleStorage.json")
#     ) as jsonFile:
#         jsonObject = json.load(jsonFile)
#         jsonFile.close()
#     # take abi/bytecode from file
#     abi = jsonObject["abi"]
#     bytecode = jsonObject["bytecode"]
#     # connect to web3
#     web3 = Web3(Web3.HTTPProvider(infura_url))
#     chain_id = 1337
#     #
#     SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
#     nonce = web3.eth.getTransactionCount(request.user.eth_address)
#     # creating contract var, that we can interact with
#     simple_storage = web3.eth.contract(address=contract_address, abi=abi)

#     return simple_storage


# def connect_to_smart_contract(request):
#     with open(
#         os.path.join(settings.BASE_DIR, "brownie/build/contracts/Ballot.json")
#     ) as jsonFile:
#         jsonObject = json.load(jsonFile)
#         jsonFile.close()
#     abi = jsonObject["abi"]
#     bytecode = jsonObject["bytecode"]
#     web3 = Web3(Web3.HTTPProvider(infura_url))
#     chain_id = 1337
#     Ballot = web3.eth.contract(abi=abi, bytecode=bytecode)
#     nonce = web3.eth.getTransactionCount(request.user.eth_address)
#     # creating contract var, that we can interact with
#     ballot = web3.eth.contract(address=contract_address, abi=abi)
#     return ballot


def deploy_contract(request):
    with open(
        os.path.join(settings.BASE_DIR, "brownie/build/contracts/BallotFactory.json")
    ) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    abi = jsonObject["abi"]
    bytecode = jsonObject["bytecode"]
    web3 = Web3(Web3.HTTPProvider(infura_url))
    chain_id = 1337
    Ballot = web3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = web3.eth.getTransactionCount(request.user.eth_address)
    # creating contract var, that we can interact with
    ballot = web3.eth.contract(address=contract_address, abi=abi)
    return ballot


@login_required
def view_proposal(request, proposal_id):

    # # interact_with_contract()
    # sm_contract = connect_to_smart_contract(request)
    # print(sm_contract.functions.getCreatorBallot())

    proposal = Proposal.objects.get(id=proposal_id)
    if request.user.id == proposal.creator.id:

        id = proposal.id
        name = proposal.long_name
        options = proposal.options.split(",")
        output = f"Proposal id {id}, name {name}"
        # return HttpResponse(output)
        return render(
            request,
            "web3app/view_proposal.html",
            {"proposal": proposal, "options": options},
        )

    else:
        return HttpResponse("Your not eligble for this proposal")


@login_required
def creating_proposal(request):
    balance = get_balance(request)
    data = Proposal.objects.all().filter(creator=request.user.id)
    if request.method == "POST":

        form = ProposalCreationForm(request.POST)
        if form.is_valid():
            print("form is valid")

            cd = form.cleaned_data

            proposal = Proposal()
            proposal.long_name = cd["long_name"]
            proposal.short_name = cd["short_name"]
            proposal.description = cd["description"]
            proposal.options = cd["options"]
            proposal.num_of_options = len(proposal.options.split(","))

            proposal.creator = request.user
            proposal.set_status(0)

            proposal.save()

            proposal_id = proposal.id

            return redirect("view_proposal", proposal_id=proposal_id)
            # return view_proposal(request, proposal_id)
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
    web3 = Web3(HTTPProvider(infura_url))
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

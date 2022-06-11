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
import web3

from .forms import ProposalCreationForm
from .models import Proposal, Web3Deploy

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


def deploy_contract(request, proposal_id):

    with open(
        os.path.join(settings.BASE_DIR, "brownie/build/contracts/BallotFactory.json")
    ) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    abi = jsonObject["abi"]
    bytecode = jsonObject["bytecode"]

    web3 = Web3(Web3.HTTPProvider(infura_url))
    chain_id = 4

    BallotFactory = web3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = web3.eth.getTransactionCount(request.user.eth_address)
    # Submit the transaction that deploys the contract
    transaction = BallotFactory.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": web3.eth.gas_price,
            "from": request.user.eth_address,
            "nonce": nonce,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(
        transaction, private_key=request.user.private_key
    )

    print("Deploying Contract!")
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print("Waiting for transaction to finish...")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

    proposal = Proposal.objects.get(id=proposal_id)
    if request.user.id == proposal.creator.id:
        deploy = Web3Deploy(creator=request.user, proposal=proposal)
        deploy.save()

    return tx_receipt.contractAddress, abi


def add_proposal_to_blockchain(request, proposal_id):
    # TO-DO
    # creating Ballot in blockchain
    # adding proposal options to Ballot.proposals
    from web3 import middleware
    from web3.middleware import geth_poa_middleware
    from web3.gas_strategies.time_based import fast_gas_price_strategy

    dep = deploy_contract(request, proposal_id)

    contract = dep[0]
    abi = dep[1]

    web3 = Web3(Web3.HTTPProvider(infura_url))
    chain_id = 4

    nonce = web3.eth.getTransactionCount(request.user.eth_address)

    proposal = Proposal.objects.get(id=proposal_id)
    prop_options = proposal.options.split("*")

    BallotFactory = web3.eth.contract(address=contract, abi=abi)
    print(f"Lenght is: {BallotFactory.functions.bfGetBallotsLenght().call()}")

    test_transaction = BallotFactory.functions.bfCreateBallot(
        0, prop_options
    ).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": web3.eth.gas_price,
            "from": request.user.eth_address,
            "nonce": nonce,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(
        test_transaction, private_key=request.user.private_key
    )
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=480)

    print(f"Lenght is: {BallotFactory.functions.bfGetBallotsLenght().call()}")

    creator = BallotFactory.functions.bfGetCreatorBallot(0).call()
    print(f"Creator is: {creator}")

    num_of_proposals = BallotFactory.functions.bfGetNumOfProposals(0).call()
    print(f"Num_of_proposals is: {num_of_proposals}")

    proposals = BallotFactory.functions.bfGetProposals(0).call()
    print(f"Proposals is: {proposals}")


def test_interact_with_contract(request, proposal_id):

    proposals = ["op1", "op2"]

    dep = deploy_contract(request, proposal_id)

    contract = dep[0]
    abi = dep[1]

    web3 = Web3(Web3.HTTPProvider(infura_url))
    chain_id = 4

    nonce = web3.eth.getTransactionCount(request.user.eth_address)

    BallotFactory = web3.eth.contract(address=contract, abi=abi)
    print(f"Lenght is: {BallotFactory.functions.bfGetBallotsLenght().call()}")

    test_transaction = BallotFactory.functions.bfCreateBallot(
        0, proposals
    ).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": web3.toWei(1200, "gwei"),
            "from": request.user.eth_address,
            "nonce": nonce + 1,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(
        test_transaction, private_key=request.user.private_key
    )
    print(signed_txn)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(tx_hash)

    print("Updating stored Value...")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)

    print(f"Lenght is: {BallotFactory.functions.bfGetBallotsLenght().call()}")


@login_required
def participation_in_proposal(request, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    creator = Proposal.objects.get(id=proposal_id).creator_id

    options = proposal.options.split("*")

    if request.method == "POST":
        pass

    else:
        return render(
            request,
            "web3app/participation_in_proposal.html",
            {"proposal": proposal, "options": options},
        )

    return render(
        request,
        "web3app/participation_in_proposal.html",
        {"proposal": proposal, "options": options},
    )


@login_required
def view_proposal(request, proposal_id):

    # print(deploy_contract(request, proposal_id))
    # test_interact_with_contract(request, proposal_id)

    proposal = Proposal.objects.get(id=proposal_id)
    if request.user.id == proposal.creator.id:
        add_proposal_to_blockchain(request, proposal_id)

        options = proposal.options.split("*")
        # return HttpResponse(output)
        return render(
            request,
            "web3app/view_proposal.html",
            {"proposal": proposal, "options": options},
        )
    if request.user.id != proposal.creator.id:
        return redirect(
            "participation_in_proposal",
            proposal_id=proposal_id,
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

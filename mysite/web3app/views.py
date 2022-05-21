from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def creating_proposal(request, proposal_id=1):
    return render(request, "web3app/creating_proposal.html")

from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from eth_account import Account
import secrets


from .forms import CustomUserCreationForm, LoginForm

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
            return HttpResponsePermanentRedirect("/login")
            # return render(request, "users/login_page.html", {"new_user": new_user})
    else:
        user_form = CustomUserCreationForm()
    return render(request, "users/registr_page.html", {"user_form": user_form})

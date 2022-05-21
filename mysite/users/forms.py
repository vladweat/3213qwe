import email
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser

from eth_account import Account
import secrets


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email",)

    def email_clean(self):
        email = self.cleaned_data["email"].lower()
        new = CustomUser.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exist")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Password don't match")
        return cd["password2"]

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            self.cleaned_data["email"], self.cleaned_data["password1"]
        )
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

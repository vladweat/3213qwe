from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "private_key",
        "eth_address",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "private_key",
        "eth_address",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        ("Account info", {"fields": ("email", "password")}),
        ("Eth", {"fields": ("private_key", "eth_address")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "private_key",
                    "eth_address",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "is_admin", "is_active", "created_at")
    list_filter = ("is_admin", "is_active", "is_staff")
    search_fields = ("username",)
    ordering = ("username",)
    # Override fieldsets — encrypted email can't be edited via raw field
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2", "is_admin")}),
    )

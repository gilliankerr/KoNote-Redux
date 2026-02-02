"""Custom user model with Azure AD and local auth support."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from konote.encryption import decrypt_field, encrypt_field


class UserManager(BaseUserManager):
    """Manager for the custom User model."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required.")
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user supporting both Azure AD SSO and local password auth.

    Roles:
        is_admin = True → full instance access (Admin role)
        UserProgramRole with role='program_manager' → manage assigned programs
        UserProgramRole with role='staff' → notes only in assigned programs
    """

    # Identity
    username = models.CharField(max_length=150, unique=True)
    external_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        help_text="Azure AD object ID for SSO users.",
    )
    display_name = models.CharField(max_length=255)
    _email_encrypted = models.BinaryField(default=b"", blank=True)

    # Roles
    is_admin = models.BooleanField(default=False, help_text="Full instance access.")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, help_text="Django admin access (rarely used).")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    # GDPR readiness
    consent_given_at = models.DateTimeField(null=True, blank=True)
    data_retention_days = models.IntegerField(default=2555, help_text="~7 years default.")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["display_name"]

    class Meta:
        app_label = "auth_app"
        db_table = "users"

    def __str__(self):
        return self.display_name or self.username

    def get_display_name(self):
        return self.display_name or self.username

    # Encrypted email property
    @property
    def email(self):
        return decrypt_field(self._email_encrypted)

    @email.setter
    def email(self, value):
        self._email_encrypted = encrypt_field(value)

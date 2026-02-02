from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "user_id", "resource_type", "event_timestamp")
    list_filter = ("action", "resource_type")
    readonly_fields = ("action", "user_id", "user_display", "resource_type",
                       "resource_id", "ip_address", "event_timestamp",
                       "old_values", "new_values", "metadata")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

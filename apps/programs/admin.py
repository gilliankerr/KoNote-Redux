from django.contrib import admin

from .models import Program, UserProgramRole


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)


@admin.register(UserProgramRole)
class UserProgramRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "program", "role")
    list_filter = ("role",)

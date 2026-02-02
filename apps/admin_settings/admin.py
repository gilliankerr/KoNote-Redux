from django.contrib import admin

from .models import FeatureToggle, InstanceSetting, TerminologyOverride


@admin.register(TerminologyOverride)
class TerminologyOverrideAdmin(admin.ModelAdmin):
    list_display = ("term_key", "display_value", "updated_at")
    search_fields = ("term_key",)


@admin.register(FeatureToggle)
class FeatureToggleAdmin(admin.ModelAdmin):
    list_display = ("feature_key", "is_enabled", "updated_at")
    list_filter = ("is_enabled",)


@admin.register(InstanceSetting)
class InstanceSettingAdmin(admin.ModelAdmin):
    list_display = ("setting_key", "setting_value", "updated_at")
    search_fields = ("setting_key",)

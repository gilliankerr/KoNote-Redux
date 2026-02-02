from django.contrib import admin

from .models import Alert, Event, EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    list_filter = ("status",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("client_file", "event_type", "title", "start_timestamp", "status")
    list_filter = ("event_type", "status")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("client_file", "status", "author", "created_at")
    list_filter = ("status",)

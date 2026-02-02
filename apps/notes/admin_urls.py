from django.urls import path

from . import admin_views

app_name = "note_templates"
urlpatterns = [
    path("", admin_views.template_list, name="template_list"),
    path("create/", admin_views.template_create, name="template_create"),
    path("<int:pk>/edit/", admin_views.template_edit, name="template_edit"),
]

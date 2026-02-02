from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    path("client/<int:client_id>/", views.note_list, name="note_list"),
    path("client/<int:client_id>/quick/", views.quick_note_create, name="quick_note_create"),
]

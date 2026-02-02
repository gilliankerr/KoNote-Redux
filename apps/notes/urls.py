from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    path("client/<int:client_id>/", views.note_list, name="note_list"),
    path("client/<int:client_id>/quick/", views.quick_note_create, name="quick_note_create"),
    path("client/<int:client_id>/new/", views.note_create, name="note_create"),
    path("<int:note_id>/", views.note_detail, name="note_detail"),
    path("<int:note_id>/cancel/", views.note_cancel, name="note_cancel"),
]

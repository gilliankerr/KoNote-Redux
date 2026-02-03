from django.urls import path

from . import views

app_name = "reports"
urlpatterns = [
    path("export/", views.export_form, name="export_form"),
    path("client/<int:client_id>/analysis/", views.client_analysis, name="client_analysis"),
]

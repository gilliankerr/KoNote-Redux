from django.urls import path
from . import views

app_name = "auth_app"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("callback/", views.azure_callback, name="azure_callback"),
    path("logout/", views.logout_view, name="logout"),
]

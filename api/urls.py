from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
    path("reset-password-request/", views.resetPasswordRequest),
    path(
        "reset-password-confirm/<str:uidb64>/<str:token>/",
        views.resetPasswordConfirm,
    ),
]

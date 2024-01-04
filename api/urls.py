from django.urls import path
from .views import auth_views, feedback_views

urlpatterns = [
    # authentication views
    path("login/", auth_views.login),
    path("register/", auth_views.register),
    path("reset-password-request/", auth_views.resetPasswordRequest),
    path(
        "reset-password-confirm/<str:uidb64>/<str:token>/",
        auth_views.resetPasswordConfirm,
    ),
    # feedback views
    path("create-feedback/<str:id>/", feedback_views.createFeedback),
]

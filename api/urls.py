from django.urls import path
from .views import auth_views, feedback_views, request_views

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
    path("get-all-feedback/<str:id>/", feedback_views.getAllFeedback),
    # request views
    path("create-request/<str:id>/", request_views.createRequest),
    path("get-all-request/<str:id>/", request_views.getAllRequest),
    # search views
]

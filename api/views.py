from rest_framework.decorators import api_view
from rest_framework.response import Response


# user authentication
@api_view(["POST"])
def login(request):
    return Response()


@api_view(["POST"])
def register(request):
    return Response()


@api_view(["POST"])
def resetPassword(request):
    return Response()


@api_view(["POST"])
def resetPasswordConfirm(request):
    return Response()

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token


# user authentication
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        # get email and password
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # control if there is a user with given email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "email"})

        # authenticate user
        user = authenticate(request, email=email, password=password)

        # control if password is correct
        if user:
            token, created = Token.objects.get_or_create(user=user)
            response = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "token": token.key,
                "registrationType": user.registrationType,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "password"})

    # unknown error
    return Response({"error": "error"})


@api_view(["POST"])
def register(request):
    return Response()


@api_view(["POST"])
def resetPassword(request):
    return Response()


@api_view(["POST"])
def resetPasswordConfirm(request):
    return Response()

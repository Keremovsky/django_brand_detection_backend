from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


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
            return Response({"response": "email"})

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
            return Response({"response": "password"})

    # unknown error
    return Response({"response": "error"})


@api_view(["POST"])
def register(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        # get email and password
        email = serializer.validated_data["email"]
        name = serializer.validated_data.get("name", "")
        password = serializer.validated_data["password"]
        registrationType = serializer.validated_data.get("registrationType", "")

        if User.objects.filter(email=email).exists():
            return Response({"response": "email"})

        newUser = User(
            email=email,
            password=make_password(password),
            name=name,
            registrationType=registrationType,
        )
        newUser.save()

        return Response({"response": "success"})

    # unknown error
    return Response({"response": "error"})


@api_view(["POST"])
def resetPassword(request):
    return Response()


@api_view(["POST"])
def resetPasswordConfirm(request):
    return Response()

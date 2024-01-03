from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .serializers import (
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from .tokens import password_reset_token_generator
from .models import User


# user authentication
@api_view(["POST"])
def login(request):
    serializer = UserSerializer(data=request.data)

    # if taken data is valid
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
    serializer = UserSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        # get email and password
        email = serializer.validated_data["email"]
        name = serializer.validated_data.get("name", "")
        password = serializer.validated_data["password"]
        registrationType = serializer.validated_data.get("registrationType", "")

        if User.objects.filter(email=email).exists():
            return Response({"response": "email"})

        # create user and save it to the database
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
def resetPasswordRequest(request):
    serializer = PasswordResetRequestSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        # get email
        email = serializer.validated_data["email"]
        # control if there is an user with given email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"response": "email"})

        # create a token for password reset
        token = password_reset_token_generator.make_token(user)

        # send mail to user email
        title = "Şifre Yenileme"
        message = f"Şifre yenileme kodunuz: {token}"
        from_email = settings.EMAIL_HOST_USER
        sent_to = [email]
        send_mail(
            title,
            message,
            from_email,
            sent_to,
            fail_silently=False,
        )

        return Response({"response": str(user.id)})

    # unknown error
    return Response({"response": "error"})


@api_view(["POST"])
def resetPasswordConfirm(request, uidb64, token):
    serializer = PasswordResetConfirmSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        # control if uidb64 is correct
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (ValueError, OverflowError, User.DoesNotExist):
            return Response({"response": "no_user"})

        # control if token is correct, if it is reset password
        if password_reset_token_generator.check_token(user, token):
            password = serializer.validated_data["password"]
            user.password = make_password(password)
            user.save()

            return Response({"response": "success"})
        else:
            return Response({"response": "token"})

    # unknown error
    return Response({"response": "error"})

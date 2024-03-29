from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django.utils.encoding import force_str
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from ..serializers import (
    UserSerializer,
    UserNameSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from ..tokens import password_reset_token_generator
from ..models import User
from ..utils.utils import saveUser
from secret import GOOGLE_CLIENT_ID


# user authentication
@api_view(["POST"])
def login(request):
    serializer = UserSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        # get email and password
        email = serializer.validated_data.get("email", "")
        password = serializer.validated_data["password"]

        # control if there is a user with given email
        try:
            user = User.objects.get(email=email)

            if user.registrationType == "google":
                # if user already registered with google
                return Response({"response": "already_google"})

        except User.DoesNotExist:
            # if there is no user with given id
            return Response({"response": "no_user"})
        except:
            return Response({"response": "error"})

        # authenticate user
        authUser = authenticate(request, email=email, password=password)
        print(authUser)

        # control if user authenticated
        if authUser:
            password, created = Token.objects.get_or_create(user=user)
            response = {
                "id": authUser.id,
                "email": authUser.email,
                "name": authUser.name,
                "token": password.key,
                "registrationType": authUser.registrationType,
            }
            return JsonResponse(
                response,
                status=status.HTTP_200_OK,
                content_type="application/json; charset=utf-8",
            )
        else:
            # if user's password is false
            return Response({"response": "password"})

    # unknown error
    return Response({"response": "error"})


@api_view(["POST"])
def signInWithGoogle(request):
    serializer = UserSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        token = serializer.validated_data["password"]
        # control if token is correct
        try:
            # get user information from google
            id_info = id_token.verify_oauth2_token(
                token, google_requests.Request(), GOOGLE_CLIENT_ID
            )
            email = id_info["email"]

            # control if there is a user with given email, if not create
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

                # if user already registered with email
                if user.registrationType == "email":
                    return Response({"response": "already_email"})

                response = {
                    "id": user.id,
                    "email": email,
                    "name": user.name,
                    "token": "",
                    "registrationType": user.registrationType,
                }
                return JsonResponse(response, status=status.HTTP_200_OK)
            else:
                # create user and save it to the database
                saveUser(email, "", id_info["name"], "google")

                user = User.objects.get(email=email)
                response = {
                    "id": user.id,
                    "email": email,
                    "name": user.name,
                    "token": "",
                    "registrationType": user.registrationType,
                }

                return JsonResponse(response, status=status.HTTP_200_OK)
        except:
            return Response({"response": "token"})

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
            # if there is an user with given email
            return Response({"response": "email"})

        # create user and save it to the database
        saveUser(email, password, name, registrationType)

        return Response({"response": "success"}, status=status.HTTP_200_OK)

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
            # if there is no user with given id
            return Response({"response": "no_user"})
        except:
            # unknown error
            return Response({"response": "error"})

        # create a token for password reset
        token = password_reset_token_generator.make_token(user)

        if user.registrationType == "google":
            return Response({"response": "google"})

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

        return JsonResponse({"response": str(user.id)}, status=status.HTTP_200_OK)

    # unknown error
    return Response({"response": "error"})


@api_view(["POST"])
def resetPasswordConfirm(request, uidb64, token):
    serializer = PasswordResetConfirmSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        # control if uidb64 is correct
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            # if there is no user with given id
            return Response({"response": "no_user"})
        except:
            # unknown error
            return Response({"response": "error"})

        # control if token is correct, if it is reset password
        if password_reset_token_generator.check_token(user, token):
            password = serializer.validated_data["password"]
            user.password = make_password(password)
            user.save()

            return Response({"response": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"response": "token"})

    # unknown error
    return Response({"response": "error"})


@api_view(["POST"])
def changeName(request, id):
    serializer = UserNameSerializer(data=request.data)

    if serializer.is_valid():
        name = serializer.validated_data["name"]
        try:
            user = User.objects.get(id=id)
            user.name = name

            print(user.password)

            user.save()

            response = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "token": user.password,
                "registrationType": user.registrationType,
            }

            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # if there is no user with given id
            return Response({"response": "no_user"})
        except:
            # unknown error
            return Response({"response": "error"})

    # unknown error
    return Response({"response": "error"})

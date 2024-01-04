from api.models import User
from django.contrib.auth.hashers import make_password


def createUser(email: str, password: str, name: str, registrationType: str):
    newUser = User(
        email=email,
        password=make_password(password),
        name=name,
        registrationType=registrationType,
    )
    newUser.save()

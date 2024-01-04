from api.models import User, HistoryModel, FeedbackModel
from django.contrib.auth.hashers import make_password


def createUser(email: str, password: str, name: str, registrationType: str):
    newUser = User(
        email=email,
        password=make_password(password),
        name=name,
        registrationType=registrationType,
    )
    newUser.save()


def createFeedback(user: User, history: HistoryModel, description: str):
    newFeedback = FeedbackModel(user=user, history=history, description=description)
    newFeedback.save()

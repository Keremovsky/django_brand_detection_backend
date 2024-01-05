from api.models import User, HistoryModel, FeedbackModel, RequestModel
from django.contrib.auth.hashers import make_password


def saveUser(email: str, password: str, name: str, registrationType: str):
    newUser = User(
        email=email,
        password=make_password(password),
        name=name,
        registrationType=registrationType,
    )
    newUser.save()


def saveFeedback(user: User, history: HistoryModel, description: str):
    newFeedback = FeedbackModel(user=user, history=history, description=description)
    newFeedback.save()


def saveRequest(user: User, request: RequestModel):
    newRequest = RequestModel(user=user, **request.__dict__)
    newRequest.save()

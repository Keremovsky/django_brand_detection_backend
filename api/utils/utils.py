import requests as r
from api.models import User, HistoryModel, FeedbackModel, RequestModel
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from secret import ENDPOINT_URL, HF_TOKEN
from typing import Optional


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


def saveRequest(user: User, requestModel: RequestModel):
    newRequest = RequestModel(user=user, **requestModel)
    newRequest.save()


def saveHistory(user: User, imageBytes: bytes, resultIds, similarities):
    newHistory = HistoryModel(user=user)

    image = ContentFile(imageBytes)
    newHistory.image.save("test.png", image)

    newHistory.setResultsIds(resultIds)
    newHistory.setSimilarities(similarities)

    newHistory.save()


def getVectorWithHug(b64Image: str):
    data = {"inputs": b64Image}
    response = r.post(
        ENDPOINT_URL,
        headers={
            "X-Wait-For-Model": "true",
            "Authorization": f"Bearer {HF_TOKEN}",
        },
        json=data,
    )

    return response


def formatHistory(
    history: HistoryModel,
    result,
    feedbackDescription: Optional[str] = None,
):
    # get similarities from sqlite
    similarities = history.getSimilarities()
    # iterate taken data from qdrant and add other needed data
    i = 0
    for res in result:
        if feedbackDescription is not None:
            res["feedbackDescription"] = feedbackDescription
        res["id"] = history.id
        res["date"] = history.date.strftime("%d/%m/%Y")
        res["searchedImage"] = history.image.url
        res["isSaved"] = history.isSaved
        res["similarity"] = similarities[i]
        i += 1

    return result

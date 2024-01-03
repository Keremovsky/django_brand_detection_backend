from django.db import models
from django.contrib.auth.models import AbstractUser
import json


# model for user data
class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    registrationType = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# model that hold old searches made by user
class HistoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="history/")
    resultIds = models.CharField(max_length=200)
    isSaved = models.BooleanField()

    # functions for store and get result ids
    def setResultsIds(self, ids):
        self.resultIds = json.dumps(ids)

    def getResultIds(self):
        return json.loads(self.resultIds)


# model that hold data for requests made by user
class RequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="request/")
    companyName = models.CharField(max_length=50)
    fileName = models.CharField(max_length=50)
    description = models.TextField()
    country = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)


# feedbacks from users about searches
class FeedbackModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.ForeignKey(HistoryModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)

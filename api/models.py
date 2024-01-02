from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    registrationType = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class HistoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="history/")
    # resultIds
    isSaved = models.BooleanField()


class RequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="request/")
    companyName = models.CharField(max_length=50)
    fileName = models.CharField(max_length=50)
    description = models.TextField()
    country = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)


class FeedbackModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.ForeignKey(HistoryModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)

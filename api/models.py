from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
import json


# custom manager for user
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# model for user data
class User(AbstractUser):
    username = None
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    registrationType = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


# model that hold old searches made by user
class HistoryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="history/")
    resultIds = models.CharField(max_length=200)
    similarities = models.CharField(max_length=200)
    isSaved = models.BooleanField(default=False)

    # functions for store and get result ids
    def setResultsIds(self, ids):
        self.resultIds = json.dumps(ids)

    def getResultIds(self):
        return json.loads(self.resultIds)

    # functions for store and get similarities
    def setSimilarities(self, sims):
        self.similarities = json.dumps(sims)

    def getSimilarities(self):
        return json.loads(self.similarities)


# model that hold data for requests made by user
class RequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="request/")
    companyName = models.CharField(max_length=50)
    description = models.TextField()
    country = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)


# feedbacks from users about searches
class FeedbackModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.ForeignKey(HistoryModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)

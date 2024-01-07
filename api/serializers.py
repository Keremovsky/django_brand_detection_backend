from rest_framework import serializers
from .models import RequestModel, HistoryModel


# user serializer
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False)
    registrationType = serializers.CharField(write_only=True, required=False)


# serializers for password reset
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


# serializers for feedback and request
class FeedbackSerializer(serializers.Serializer):
    historyId = serializers.CharField()
    description = serializers.CharField()


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestModel
        exclude = ["user", "date"]


# history serializers
class HistoryIdSerializer(serializers.Serializer):
    id = serializers.CharField()


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = "__all__"

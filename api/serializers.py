from rest_framework import serializers
from .models import RequestModel, HistoryModel


# user serializer
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(read_only=True)
    registrationType = serializers.CharField(write_only=True)


# serializers for password reset
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


# serializers for feedback and request
class FeedbackSerializer(serializers.Serializer):
    historyId = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestModel
        exclude = ["user", "date"]


# history serializers
class HistoryIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = "__all__"

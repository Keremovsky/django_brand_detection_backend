from rest_framework import serializers
from .models import User, RequestModel, FeedbackModel


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class FeedbackSerializer(serializers.Serializer):
    historyId = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)


class RequestSerializer(serializers.Serializer):
    class Meta:
        model = RequestModel
        fields = "__all__"

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(read_only=True)
    registrationType = serializers.CharField(write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class FeedbackSerializer(serializers.Serializer):
    historyId = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)

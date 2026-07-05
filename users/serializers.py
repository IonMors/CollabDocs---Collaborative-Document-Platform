from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        validate_password(attrs["password"])

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data.get(
                "first_name",
                ""
            ),
            last_name=validated_data.get(
                "last_name",
                ""
            ),
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user
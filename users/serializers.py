from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from assessments.models import Assessments

from .models import User


class AssessmentsShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessments
        fields = [
            "comment",
            "stars",
            "user",
            "book",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "username",
            "email",
            "password",
            "books",
            "lending",
            "created_at",
            "assessments",
        ]
        read_only_fields = ["books", "created_at"]
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
            "password": {"write_only": True},
        }
        depth = 1

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(instance.password)
        serializer = UserSerializer(
            instance,
            data=validated_data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        instance.save()

        return instance


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "username",
            "email",
            "password",
            "status",
            "books",
            "lending",
            "created_at",
            "unblocked_date",
        ]
        read_only_fields = ["books", "created_at", "lendings"]
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(instance.password)
        serializer = UserSerializer(
            instance,
            data=validated_data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        instance.save()

        return instance


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "type_user",
            "username",
            "email",
            "password",
            "status",
            "Books",
            "Created_at",
        ]
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
            "Books": {"read_only": True},
            "status": {"read_only": True},
            "Created_at": {"read_only": True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(instance.password)
        serializer = UserSerializer(instance, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance.save()

        return instance

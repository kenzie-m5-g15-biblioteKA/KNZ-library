from rest_framework import serializers
from users.serializers import UserShortSerializer
from .models import Lending


class LendingsCreateSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Lending
        fields = [
            "id",
            "created_at",
            "return_date",
            "returned_date",
            "traffic_ticket",
            "user",
            "copy",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "copy": {"read_only": True},
            "created_at": {"read_only": True},
            "return_date": {"read_only": True},
        }
        depth = 2


class LendingsUpdateSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Lending
        fields = [
            "id",
            "created_at",
            "return_date",
            "returned_date",
            "traffic_ticket",
            "user",
            "copy",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "copy": {"read_only": True},
            "created_at": {"read_only": True},
        }
        depth = 2

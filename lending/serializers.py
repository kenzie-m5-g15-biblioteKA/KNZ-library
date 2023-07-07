from rest_framework import serializers
from users.serializers import UserShortSerializer
from .models import Lending


class LendingsSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    def create(self, validated_data):
        return Lending.objects.create(**validated_data)

    class Meta:
        model = Lending
        fields = [
            "id",
            "created_at",
            "return_date",
            "returned_date",
            "user",
            "copy",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "copy": {"read_only": True},
            "return_date": {"read_only": True},
        }
        depth = 2

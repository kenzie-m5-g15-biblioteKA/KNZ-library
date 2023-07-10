from rest_framework import serializers

from users.serializers import UserShortSerializer

from .models import Lending


class LendingSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        for _, field in fields.items():
            field.read_only = True
        return fields

    class Meta:
        model = Lending
        fields = "__all__"
        depth = 2

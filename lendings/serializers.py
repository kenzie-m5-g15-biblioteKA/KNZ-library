from rest_framework import serializers

from .models import Lending


class LendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending
        fields = "__all__"
        read_only_fields = ["lend_date", "return_date", "returned_date", "status"]

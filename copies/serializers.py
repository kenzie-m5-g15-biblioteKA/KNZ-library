from rest_framework import serializers

from copies.models import Copy


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = [
            "id",
            "copies",
            "book",
            "description",
        ]
        read_only_field = ["book"]
        depth = 1

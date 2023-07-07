from rest_framework import serializers
from copy_book.models import Copy


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = [
            "id",
            "copies",
            "lending",
            "book",
            "description",
        ]
        depth = 1
        extra_kwargs = {
            "lending": {"read_only": True},
            "book": {"read_only": True},
        }

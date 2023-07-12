from rest_framework import serializers
from books.serializers import BookShortSerializer
from users.serializers import UserShortSerializer
from .models import Assessments


class AssessmentsSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    book = BookShortSerializer(read_only=True)

    class Meta:
        model = Assessments
        fields = [
            "id",
            "comment",
            "stars",
            "user",
            "book",
        ]

        depth = 1

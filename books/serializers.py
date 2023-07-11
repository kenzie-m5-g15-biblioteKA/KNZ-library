from rest_framework import serializers
from users.serializers import UserShortSerializer
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    followers = UserShortSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "published_date",
            "publishing_company",
            "availability",
            "ranking",
            "assessments",
            "followers",
        ]
        depth = 1
        extra_kwargs = {"followers": {"read_only": True}}


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
        ]

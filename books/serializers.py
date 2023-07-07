from rest_framework import serializers

from users.serializers import UserShortSerializer

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    followers = UserShortSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["followers"]
        depth = 1


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
        ]

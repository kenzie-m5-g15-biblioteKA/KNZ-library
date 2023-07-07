from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Book


class BooksSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, data):
    #     user = data.user
    #     serializer = UserSerializer(user)
    #     return serializer.data

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    class Meta:
        model = Book
        fields = [
            "id",
            "name",
            "published_date",
            "followers",
        ]
        extra_kwargs = {"followers": {"read_only": True}}

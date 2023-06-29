from rest_framework import serializers
from .models import Books
from users.serializers import UserSerializer


class BooksSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, data):
    #     user = data.user
    #     serializer = UserSerializer(user)
    #     return serializer.data

    def create(self, validated_data):
        return Books.objects.create(**validated_data)

    class Meta:
        model = Books
        fields = [
            "id",
            "name",
            "published_date",
            "followers",
        ]
        extra_kwargs = {"followers": {"read_only": True}}

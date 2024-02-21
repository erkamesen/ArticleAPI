from rest_framework import serializers
from api.models import (
    Author,
    Tag,
    Post
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def validate_email(self, value):
        is_exist = Author.objects.filter(email=value).exists()
        if is_exist:
            raise serializers.ValidationError("This email is already exists.")
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

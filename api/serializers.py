from rest_framework import serializers
from api.models import (
    Author,
    Tag,
    Post
)
from django.shortcuts import get_object_or_404


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=255)

    def create(self, validated_data):
        author = Author.objects.create(**validated_data)
        return author

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance

    def validate_email(self, value):
        is_exist = Author.objects.filter(email=value).exists()
        if is_exist:
            raise serializers.ValidationError("This email is already exists.")
        return value


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        tag = Tag.objects.create(**validated_data)
        return tag

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)

    author_id = serializers.IntegerField(write_only=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False)

    def create(self, validated_data):
        author_id = validated_data.pop("author_id")
        tag_ids = validated_data.pop("tag_ids", [])

        author = get_object_or_404(Author, id=author_id)

        post = Post.objects.create(author=author, **validated_data)

        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)
        else:
            post.tags.clear()

        return post

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)

        if 'author_id' in validated_data:
            author_id = validated_data.pop('author_id')
            instance.author = get_object_or_404(Author, id=author_id)

        if tag_ids is not None:
            instance.tags.clear()
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)

        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance

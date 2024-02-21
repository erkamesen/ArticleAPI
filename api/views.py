from api.models import Author, Post, Tag
from api.serializers import AuthorSerializer, TagSerializer, PostSerializer
from rest_framework import viewsets
# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class TagViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer
    queryset = Post.objects.all()

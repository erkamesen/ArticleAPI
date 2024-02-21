from api.models import Author, Post, Tag
from api.serializers import AuthorSerializer, TagSerializer, PostSerializer
from rest_framework import generics
# Create your views here.


class AuthorAPIView(generics.ListCreateAPIView):

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class TagAPIView(generics.ListCreateAPIView):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PostAPIView(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()

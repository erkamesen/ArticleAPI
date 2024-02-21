from rest_framework.views import APIView
from api.models import Author, Post, Tag
from api.serializers import AuthorSerializer, TagSerializer, PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
# Create your views here.


class AuthorAPIView(APIView):

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class AuthorDetailAPIView(APIView):

    def get_object(self, pk):
        author = get_object_or_404(Author, pk=pk)
        return author

    def get(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagAPIView(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TagDetailAPIView(APIView):

    def get_object(self, pk):
        tag = get_object_or_404(Tag, pk=pk)
        return tag

    def get(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):

    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

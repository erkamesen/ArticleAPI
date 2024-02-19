"""
Tests for POST API
"""

from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from api.models import Post, Author, Tag
from rest_framework import status


LIST_POST_URL = reverse("api:posts")


def create_author(name="testname", surname="testsurname",
                  email="test@example.com", phone="123123123"):
    author = Author.objects.create(name=name, surname=surname,
                                   email=email, phone=phone)
    return author


def create_tag(name="test_tag"):
    tag = Tag.objects.create(name=name)
    return tag


def create_post(title="test_title", content="test_content"):
    author = create_author()
    tag = create_tag()
    post = Post.objects.create(author=author, title=title, content=content)
    post.tags.add(tag)
    return post


def detail_url(post_id):
    return reverse("api:posts-detail", args=[post_id,])


class PostTests(TestCase):
    """Tests for POST model"""

    def setUp(self):
        self.client = APIClient()

    def test_list_posts(self):
        """Test for list all posts in database"""
        create_post()

        res = self.client.get(LIST_POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_post_with_correct_credentials(self):  # Positive
        """Test create post succesfully"""
        create_author()
        create_tag()
        payload = {
            "title": "Test Title",
            "content": "Test Content",
            "author_id": 1,
            "tag_ids": [1],
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("title"), payload.get("title"))

    def test_create_post_with_wrong_credentials(self):  # Negative
        """Test create post and get 400 status code"""
        payload = {
            "title": "Test Title",
            "content": "Test Content",
            "tag_ids": [1],
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_post_detail(self):
        """Test retrieve spesific post details"""
        post = create_post()
        url = detail_url(post.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("title"), post.title)

    def test_put_post_succesfully(self):  # Positive
        """Test put method in post infos"""
        post = create_post()

        url = detail_url(post.id)

        payload = {
            "title": "New Title",
            "content": "New Content",
            "author_id": 1,
            "tag_ids": [1],
        }

        res = self.client.put(url, data=payload)

        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(post.title, payload.get("title"))

    def test_put_post_failure(self):  # Negative
        """Test put method in post infos"""
        post = create_post()
        url = detail_url(post.id)

        payload = {

        }

        res = self.client.put(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_post_succesfully(self):
        """Test patch method in post infos"""

        post = create_post()
        url = detail_url(post.id)

        payload = {
            "title": "New Title",
        }

        res = self.client.patch(url, data=payload)

        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("title"), post.title)

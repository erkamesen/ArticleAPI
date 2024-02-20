"""
Tests for TAG API
"""

from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from api.models import Tag
from rest_framework import status


LIST_POST_URL = reverse("api:tags")


def create_tag(name="test_tag"):
    tag = Tag.objects.create(name=name)
    return tag


def create_tags(lim=5):
    tags = [Tag(name=f"test_tag{i}") for i in range(1, lim + 1)]
    Tag.objects.bulk_create(tags)


def detail_url(tag_id):
    return reverse("api:tags-detail", args=[tag_id,])


class TagTests(TestCase):
    """Tests for TAG model"""

    def setUp(self):
        self.client = APIClient()

    def test_list_tags(self):
        """Test for list all tags in database"""
        create_tags(3)

        res = self.client.get(LIST_POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_create_tag_with_correct_credentials(self):  # Positive
        """Test create tag succesfully"""
        payload = {
            "name": "Test-Tag",
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get("name"), payload.get("name"))

    def test_create_tag_with_wrong_credentials(self):  # Negative
        """Test create tag and get 400 status code"""
        payload = {
        }

        res = self.client.post(LIST_POST_URL, data=payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_tag_detail(self):
        """Test retrieve spesific tag details"""
        tag = create_tag()
        url = detail_url(tag.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), tag.name)

    def test_put_tag_succesfully(self):  # Positive
        """Test put method in tag infos"""
        tag = create_tag()
        url = detail_url(tag.id)

        payload = {
            "name": "New Name",
        }

        res = self.client.put(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_tag_failure(self):  # Negative
        """Test put method in tag infos"""
        tag = create_tag()
        url = detail_url(tag.id)

        payload = {

        }

        res = self.client.put(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_tag_succesfully(self):
        """Test patch method in atuhor infos"""

        tag = create_tag()
        url = detail_url(tag.id)

        payload = {
            "name": "New Tag",
        }

        res = self.client.patch(url, data=payload)

        tag.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("name"), tag.name)

    def test_delete_patch(self):
        """Test delete tag api"""
        tag = create_tag()
        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

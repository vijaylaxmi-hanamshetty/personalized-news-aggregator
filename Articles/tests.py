from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from Articles.models import Articles
from News.models import News
from Categories.models import Categories
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ArticlesAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone="+919999999999", password="testpass123", name="Test User", role="user"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Categories.objects.create(name="Test Category")
        self.news = News.objects.create(name="Test Source")
        self.article = Articles.objects.create(
            title="Test Article",
            content="Test Content",
            summary="Test Summary",
            url="https://example.com/article",
            published_at=timezone.now(),
            source=self.news,
            category=self.category,
            language="en"
        )
        self.list_url = reverse("articles-list")
        self.detail_url = reverse("articles-detail", args=[self.article.id])

    def test_list_articles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_article(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.article.id)

    def test_create_article(self):
        data = {
            "title": "New Article",
            "content": "New Content",
            "summary": "New Summary",
            "url": "https://example.com/new",
            "published_at": timezone.now().isoformat(),
            "source": self.news.id,
            "category": self.category.id,
            "language": "en"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Articles.objects.filter(title="New Article").exists())

    def test_update_article(self):
        data = {
            "title": "Updated Title"
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Updated Title")

    def test_delete_article(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Articles.objects.filter(id=self.article.id).exists())
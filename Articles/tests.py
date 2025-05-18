from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from Articles.models import Articles
from News.models import News
from Categories.models import Categories
from django.contrib.auth import get_user_model

class ArticlesCRUDTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            phone="+919999999999", password="testpass123", name="Test User", role="user"
        )
        self.client.force_authenticate(user=self.user)
        self.news = News.objects.create(
            name="Test News",
            url="https://news.com",
            category="general",
            language="en",
            logo_url="https://news.com/logo.png"
        )
        self.category = Categories.objects.create(
            name="Tech",
            slug="tech"
        )
        self.articles_data = {
            "title": "Test Article",
            "content": "This is the content.",
            "summary": "Summary here.",
            "url": "https://news.com/article",
            "published_at": "2024-01-01T10:00:00Z",
            "source": self.news.id,
            "category": self.category.id,
            "language": "en"
        }
        self.article = Articles.objects.create(
            title="Test Article",
            content="This is the content.",
            summary="Summary here.",
            url="https://news.com/article",
            published_at="2024-01-01T10:00:00Z",
            source=self.news,
            category=self.category,
            language="en"
        )
        self.list_url = reverse('articles-list')
        self.detail_url = reverse('articles-detail', args=[self.article.id])

    def test_list_articles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_article(self):
        data = self.articles_data.copy()
        data["url"] = "https://news.com/article2"
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_retrieve_article(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.articles_data["title"])

    def test_update_article(self):
        data = self.articles_data.copy()
        data["title"] = "Updated Article"
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Article")

    def test_partial_update_article(self):
        response = self.client.patch(self.detail_url, {"summary": "Partial update"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["summary"], "Partial update")

    def test_delete_article(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Articles.objects.filter(id=self.article.id).exists())
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Articles.models import Articles
from News.models import News
from Categories.models import Categories
from Savearticles.models import SavedArticles
from django.utils import timezone

User = get_user_model()

class SavedArticlesAPITestCase(TestCase):
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
        self.list_url = reverse("saved-articles-list")

    def test_user_can_save_article(self):
        response = self.client.post(self.list_url, {'article': self.article.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SavedArticles.objects.count(), 1)

    

    def test_user_can_view_own_saved_articles(self):
        SavedArticles.objects.create(user=self.user, article=self.article)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_cannot_delete_saved_article(self):
        saved = SavedArticles.objects.create(user=self.user, article=self.article)
        detail_url = reverse("saved-articles-detail", args=[saved.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
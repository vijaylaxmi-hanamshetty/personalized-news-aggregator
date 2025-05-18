from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Articles.models import Articles
from Savearticles.models import SavedArticles

class SavedArticlesAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user2 = User.objects.create_user(username="otheruser", password="testpass")
        self.article = Articles.objects.create(title="Test Article", content="Test Content")
        self.article2 = Articles.objects.create(title="Another Article", content="More Content")
        self.saved_article = SavedArticles.objects.create(user=self.user, article=self.article)
        self.client = APIClient()
        self.url = reverse('savedarticles-list')  # Adjust if your router uses a different basename

    def test_list_saved_articles_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_saved_articles_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_saved_article(self):
        self.client.force_authenticate(user=self.user)
        data = {"article": self.article2.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["article"], self.article2.id)

    def test_create_saved_article_unauthenticated(self):
        data = {"article": self.article2.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_saved_article(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('savedarticles-detail', args=[self.saved_article.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.saved_article.id)

    def test_retrieve_saved_article_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        detail_url = reverse('savedarticles-detail', args=[self.saved_article.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_saved_article(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('savedarticles-detail', args=[self.saved_article.id])
        data = {"article": self.article2.id}
        response = self.client.put(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["article"], self.article2.id)

    def test_partial_update_saved_article(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('savedarticles-detail', args=[self.saved_article.id])
        data = {"article": self.article2.id}
        response = self.client.patch(detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["article"], self.article2.id)

    def test_delete_saved_article(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('savedarticles-detail', args=[self.saved_article.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
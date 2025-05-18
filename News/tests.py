from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from News.models import News
from django.contrib.auth import get_user_model
from unittest.mock import patch

class NewsCRUDTestCase(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            phone="+919999999999", password="testpass123", name="Test User", role="user"
        )
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse('news-list')
        self.news_data = {
            "name": "Test Source",
            "url": "https://example.com/article1",
            "category": "technology",
            "language": "en",
            "logo_url": "https://example.com/image1.jpg",
        }
        self.news = News.objects.create(**self.news_data)
        self.detail_url = reverse('news-detail', args=[self.news.id])

    def test_list_news(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_news(self):
        data = {
            "name": "Another Source",
            "url": "https://example.com/article2",
            "category": "science",
            "language": "en",
            "logo_url": "https://example.com/image2.jpg",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_retrieve_news(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.news_data["name"])

    def test_update_news(self):
        data = self.news_data.copy()
        data["name"] = "Updated Source"
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Source")

    def test_partial_update_news(self):
        response = self.client.patch(self.detail_url, {"category": "health"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category"], "health")

    def test_delete_news(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(News.objects.filter(id=self.news.id).exists())

    @patch("News.views.requests.get")
    def test_fetch_news_action(self, mock_get):
        # Mock NewsAPI response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "articles": [
                {
                    "source": {"name": "Test Source"},
                    "url": "https://example.com/article1",
                    "urlToImage": "https://example.com/image1.jpg"
                }
            ]
        }
        fetch_url = reverse('news-fetch-news')
        response = self.client.get(fetch_url, {"q": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertTrue("1 articles" in response.data["message"])
        self.assertTrue(News.objects.filter(url="https://example.com/article1").exists())
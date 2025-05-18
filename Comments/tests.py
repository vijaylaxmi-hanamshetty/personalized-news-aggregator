from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from Articles.models import Articles
from Comments.models import Comments
from Categories.models import Categories
from News.models import News  # <-- Add this import

class CommentsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            phone="+919999999999", password="testpass123", name="Test User", role="user"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Categories.objects.create(name="Test Category", slug="test-category")
        self.news = News.objects.create(
            name="Test News",
            url="https://news.com",
            category="general",
            language="en",
            logo_url="https://news.com/logo.png"
        )
        self.article = Articles.objects.create(
            title="Test Article",
            content="Some content",
            published_at="2024-01-01T10:00:00Z",
            category=self.category,
            source=self.news,  # <-- Required field
        )
        self.comment = Comments.objects.create(
            user=self.user, article=self.article, comment_text="Nice article!"
        )

    def test_list_comments(self):
        response = self.client.get(reverse('comments-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Nice article!', str(response.data))

    def test_retrieve_comment(self):
        response = self.client.get(reverse('comments-detail', args=[self.comment.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment_text'], "Nice article!")

    def test_create_comment(self):
        data = {
            "article": self.article.id,
            "comment_text": "Another comment"
        }
        response = self.client.post(reverse('comments-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment_text'], "Another comment")

    def test_update_comment(self):
        data = {
            "article": self.article.id,
            "comment_text": "Updated comment"
        }
        response = self.client.put(reverse('comments-detail', args=[self.comment.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment_text'], "Updated comment")

    def test_delete_comment(self):
        response = self.client.delete(reverse('comments-detail', args=[self.comment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_not_allowed(self):
        data = {"comment_text": "Partial update"}
        response = self.client.patch(reverse('comments-detail', args=[self.comment.id]), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
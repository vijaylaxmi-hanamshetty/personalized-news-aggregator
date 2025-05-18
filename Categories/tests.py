from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from Categories.models import Categories
from django.contrib.auth import get_user_model

class CategoriesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='testuser', password='testpass', role='user', phone='+919999999999'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Categories.objects.create(name="Science", slug="science")

    def test_list_categories(self):
        response = self.client.get(reverse('categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Science', str(response.data))

    def test_retrieve_category(self):
        response = self.client.get(reverse('categories-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Science")

    def test_create_category(self):
        data = {"name": "Health", "slug": "health"}
        response = self.client.post(reverse('categories-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Health")

    def test_update_category(self):
        data = {"name": "Updated Science", "slug": "science"}
        response = self.client.put(reverse('categories-detail', args=[self.category.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Science")

    def test_delete_category(self):
        response = self.client.delete(reverse('categories-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_not_allowed(self):
        data = {"name": "Partial Update"}
        response = self.client.patch(reverse('categories-detail', args=[self.category.id]), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
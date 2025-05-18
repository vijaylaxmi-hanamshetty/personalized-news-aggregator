from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from Profile.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

User = get_user_model()


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone="+919999999999", password="testpass123", name="Test User", role="user"
        )
        self.client.force_authenticate(user=self.user)
        self.create_url = reverse("profile-create")
        self.detail_url = reverse("profile-detail")

    def test_create_profile_with_image(self):
     image_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00'
        b'\x00\x00\nIDATx\xdac\xf8\x0f\x00\x01\x01\x01\x00'
        b'\x18\xdd\x8d\xe1\x00\x00\x00\x00IEND\xaeB`\x82'
    )
     image = SimpleUploadedFile(
        "test.png", image_data, content_type="image/png"
    )
     data = {
        "bio": "Hello, I am a test user.",
        "location": "Test City",
        "birth_date": "2000-01-01",
        "profile_picture": image,
    }
     response = self.client.post(self.create_url, data, format="multipart")
     print(response.data)
     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
     self.assertIn("profile_picture", response.data)
     self.assertTrue(response.data["profile_picture"].endswith("test.png"))
    def test_get_profile(self):
        Profile.objects.create(user=self.user, bio="Bio", location="Loc")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["bio"], "Bio")

    def test_update_profile_image(self):
        profile = Profile.objects.create(user=self.user, bio="Old Bio")
        new_image = SimpleUploadedFile(
            "new.jpg", b"new_content", content_type="image/jpeg"
        )
        data = {
            "bio": "Updated Bio",
            "location": "New City",
            "birth_date": "1999-12-31",
            "profile_picture": new_image,
        }
        response = self.client.put(self.detail_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Updated Bio")
        self.assertTrue(response.data["profile_picture"].endswith("new.jpg"))

    def test_partial_update_profile(self):
        Profile.objects.create(user=self.user, bio="Old Bio")
        data = {"bio": "Partially Updated Bio"}
        response = self.client.patch(self.detail_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Partially Updated Bio")

    def test_delete_profile(self):
        Profile.objects.create(user=self.user, bio="To be deleted")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(user=self.user).exists())

    
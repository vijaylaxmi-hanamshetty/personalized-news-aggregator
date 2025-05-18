from rest_framework import generics, permissions
from Profile.serializers import ProfileSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser

class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=ProfileSerializer,
        responses=ProfileSerializer,
        description="Create profile (multipart/form-data with image upload)"
    )
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        responses=ProfileSerializer,
        description="Get, update, or delete the authenticated user's profile"
    )
    def get_object(self):
        return self.request.user.profile
    
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
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
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        if partial:
            return self.partial_update(request, *args, **kwargs)
        else:
            return self.full_update(request, *args, **kwargs)

    def full_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
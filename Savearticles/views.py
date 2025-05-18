from rest_framework import viewsets, permissions, status
from Savearticles.models import SavedArticles
from Savearticles.serializer import SavedArticlesSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response


@extend_schema(tags=["Saved Articles"])
class SavedArticleViewSet(viewsets.ModelViewSet):
    serializer_class = SavedArticlesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return SavedArticles.objects.filter(user=user)
        return SavedArticles.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Deleting saved articles ."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    
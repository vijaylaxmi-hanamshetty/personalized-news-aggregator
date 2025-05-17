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

    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()

        if not article:
            return Response({"detail": "Article not Found"})

            return Response(
                {
                    "message": "Custom message",
                    "article": SavedArticlesSerializer(article).data,
                }
            )

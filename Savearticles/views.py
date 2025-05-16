from rest_framework import viewsets, permissions
from Savearticles.models import SavedArticles
from  Savearticles.serializer import SavedArticlesSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Saved Articles"])
class SavedArticleViewSet(viewsets.ModelViewSet):
    queryset = SavedArticles.objects.all()
    serializer_class = SavedArticlesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the user from the request
        serializer.save(user=self.request.user)

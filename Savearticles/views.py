from rest_framework import viewsets, permissions
from Savearticles.models import SavedArticles
from  Savearticles.serializer import SavedArticleSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Saved Articles"])
class SavedArticleViewSet(viewsets.ModelViewSet):
    queryset = SavedArticles.objects.all()
    serializer_class = SavedArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the user from the request
        serializer.save(user=self.request.user)

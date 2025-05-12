from rest_framework import viewsets, permissions
from Comments.models import Comments
from Comments.serializer import CommentSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Comments"])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the user from the request
        serializer.save(user=self.request.user)

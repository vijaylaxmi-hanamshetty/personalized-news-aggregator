from rest_framework import viewsets, permissions
from Comments.models import Comments
from Comments.serializer import CommentsSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Comments"])
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

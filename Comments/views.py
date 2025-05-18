from rest_framework import viewsets, permissions, mixins,status
from Comments.models import Comments
from Comments.serializer import CommentsSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

@extend_schema(tags=["Comments"])
class CommentsViewSet(
    viewsets.mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PATCH" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

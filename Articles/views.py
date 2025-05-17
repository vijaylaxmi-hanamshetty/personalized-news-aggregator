from rest_framework import viewsets,status
from Articles.models import Articles
from Articles.serializer import ArticleSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
@extend_schema(tags=["Articles"])
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer
def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True 
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
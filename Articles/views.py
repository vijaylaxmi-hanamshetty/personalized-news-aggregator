from rest_framework import viewsets
from Articles.models import Articles
from Articles.serializer import ArticleSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Articles"])
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

from rest_framework import viewsets
from Categories.models import Categories
from Categories.serializer import CategorySerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response

@extend_schema(
    tags=["Categories"],
    parameters=[
        OpenApiParameter(name='name', description='Filter categories by name', required=False, type=str),
    ]
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

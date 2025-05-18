from rest_framework import viewsets,mixins,status
from Categories.models import Categories
from Categories.serializer import CategoriesSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response

@extend_schema(
    tags=["Categories"],
    parameters=[
        OpenApiParameter(name='name', description='Filter categories by name', required=False, type=str),
    ]
)
class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PATCH" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
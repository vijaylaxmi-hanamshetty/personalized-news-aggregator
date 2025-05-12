from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Categories.views import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]

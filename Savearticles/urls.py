from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Savearticles.views import SavedArticleViewSet

router = DefaultRouter()
router.register(r'saved-articles', SavedArticleViewSet, basename='saved-articles')

urlpatterns = [
    path('', include(router.urls)),
]

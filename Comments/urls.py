from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Comments.views import CommentViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]

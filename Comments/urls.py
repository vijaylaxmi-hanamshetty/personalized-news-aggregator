from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Comments.views import CommentsViewSet

router = DefaultRouter()
router.register(r'comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]

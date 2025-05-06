from django.urls import path
from .views import ProfileCreateView, ProfileDetailView

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='profile-create'),
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
]

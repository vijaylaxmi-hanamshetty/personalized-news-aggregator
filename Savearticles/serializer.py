from rest_framework import serializers
from Savearticles.models import SavedArticles


class SavedArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedArticles
        fields = '__all__'
        
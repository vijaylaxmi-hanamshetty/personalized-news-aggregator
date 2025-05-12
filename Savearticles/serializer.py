from rest_framework import serializers
from Savearticles.models import SavedArticles
from Articles.serializer import ArticleSerializer

class SavedArticlesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    article = ArticleSerializer(read_only=True) 
    class Meta:
        model = SavedArticles
        fields = '__all__'
        
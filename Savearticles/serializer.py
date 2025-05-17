from rest_framework import serializers
from Savearticles.models import SavedArticles
from Articles.serializer import ArticleSerializer
from Articles.models import Articles
class SavedArticlesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    article = serializers.PrimaryKeyRelatedField(queryset=Articles.objects.all())  
    class Meta:
        model = SavedArticles
        fields = '__all__'
        read_only_fields = ['user', 'saved_at']
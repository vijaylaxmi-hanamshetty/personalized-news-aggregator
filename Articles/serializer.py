from rest_framework import serializers
from Articles.models import Articles
from django.contrib.auth import authenticate


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'
        
from rest_framework import serializers
from Comments.models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    article = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'
    read_only_fields = ['user', 'timestamp']   
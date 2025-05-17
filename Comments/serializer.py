from rest_framework import serializers
from Comments.models import Comments
from Articles.models import Articles

class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    article = serializers.PrimaryKeyRelatedField(queryset=Articles.objects.all())
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']   
# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            phone=validated_data['phone'],
            name=validated_data['name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])  # 🔐 Hash the password
        user.save()
        return user

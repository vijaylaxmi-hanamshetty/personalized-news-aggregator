from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "name", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            phone=validated_data["phone"],
            name=validated_data["name"],
            role=validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        user = User.objects.filter(phone=phone).first()
        if user is None:
            raise ValidationError("User with this phone number does not exist.")

        if not user.check_password(password):
            raise ValidationError("Invalid password.")

        return attrs

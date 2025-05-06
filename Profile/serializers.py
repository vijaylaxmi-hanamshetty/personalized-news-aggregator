from rest_framework import serializers
from Profile.models import Profile
from django.core.exceptions import ValidationError


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "profile_picture", "location", "birth_date"]
        read_only_fields= ["id", "user"]
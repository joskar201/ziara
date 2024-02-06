from rest_framework import serializers
from .models import UserProfile, Destination


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'user_type', 'phone_number', 'bio', 'profile_pic']


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'location', 'destination_type', 'popular_activities', 'image']

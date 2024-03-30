from rest_framework import serializers
from .models import (
    UserProfile, Destination, Activity, Booking, 
    Itinerary, ItineraryItem, VisaRequirement, 
    Checklist, ChecklistItem, Transfer
    )
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'travel_preferences', 'booking_history')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            travel_preferences=validated_data['travel_preferences'],
            booking_history=validated_data['booking_history']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    activity_details = ActivitySerializer(source='activity', read_only=True)
    accomodation_details = DestinationSerializer(source='destination', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user_profile',)

    def __init__(self, *args, **kwargs):
        super(BookingSerializer, self).__init__(*args, **kwargs)
        # Dynamically add extra fields to the serializer.
        self.fields['activity_details'] = ActivitySerializer(read_only=True, source='activity')
        self.fields['accomodation_details'] = DestinationSerializer(read_only=True, source='destination')


class ItineraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = '__all__'

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = '__all__'
        read_only_fields = ('user_profile',)

class VisaRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaRequirement
        fields = '__all__'

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'
        read_only_fields = ('user_profile',)

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        read_only_fields = ('user_profile',)
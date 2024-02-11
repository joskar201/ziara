from rest_framework import viewsets
from .models import UserProfile, Destination, Activity, Booking, Itinerary, ItineraryItem
from .serializers import UserProfileSerializer, DestinationSerializer, ActivitySerializer, BookingSerializer, ItinerarySerializer, ItineraryItemSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class ItineraryItemViewSet(viewsets.ModelViewSet):
    queryset = ItineraryItem.objects.all()
    serializer_class = ItineraryItemSerializer

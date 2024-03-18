from rest_framework import viewsets
from .models import UserProfile, Destination, Activity, Booking, Itinerary, ItineraryItem
from .serializers import UserProfileSerializer, DestinationSerializer, ActivitySerializer, BookingSerializer, ItinerarySerializer, ItineraryItemSerializer
from rest_framework.permissions import IsAuthenticated


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ItineraryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class ItineraryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ItineraryItem.objects.all()
    serializer_class = ItineraryItemSerializer

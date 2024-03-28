from rest_framework import viewsets, status, views
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import (
    UserProfile, Destination, Activity, Booking, Itinerary, 
    ItineraryItem, VisaRequirement, Checklist, ChecklistItem,Transfer
    )
from .serializers import (
    UserProfileSerializer, DestinationSerializer, ActivitySerializer, 
    BookingSerializer, ItinerarySerializer, ItineraryItemSerializer, 
    UserRegistrationSerializer, VisaRequirementSerializer, 
    ChecklistSerializer, ChecklistItemSerializer, TransferSerializer
    )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['User Registration'],
    summary='Register a new user',
    description='This endpoint registers a new user with the provided information.',
    request=UserRegistrationSerializer,
    responses={201: UserRegistrationSerializer}
)
class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)

    def get_queryset(self):
        # Return bookings only for the authenticated user
        return Booking.objects.filter(user_profile=self.request.user.userprofile)

class ItineraryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)

    def get_queryset(self):
        return Itinerary.objects.filter(user_profile=self.request.user.userprofile)


class ItineraryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItineraryItemSerializer

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return ItineraryItem.objects.filter(itinerary__user_profile=user_profile)


class VisaRequirementViewSet(ReadOnlyModelViewSet):
    queryset = VisaRequirement.objects.all()
    serializer_class = VisaRequirementSerializer

class ChecklistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChecklistSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)

    def get_queryset(self):
        return Checklist.objects.filter(user_profile=self.request.user.userprofile)

class ChecklistItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChecklistItemSerializer

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return ChecklistItem.objects.filter(checklist__user_profile=user_profile)


class TransferViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def perform_create(self, serializer):
        # Automatically set the user_profile to the authenticated user's profile
        serializer.save(user_profile=self.request.user.userprofile)

    def get_queryset(self):
        # Return transfers only for the authenticated user's profile
        return Transfer.objects.filter(user_profile=self.request.user.userprofile)
from rest_framework import viewsets, status, views
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import UserProfile, Destination, Activity, Booking, Itinerary, ItineraryItem, VisaRequirement, Checklist, ChecklistItem
from .serializers import UserProfileSerializer, DestinationSerializer, ActivitySerializer, BookingSerializer, ItinerarySerializer, ItineraryItemSerializer, UserRegistrationSerializer, VisaRequirementSerializer, ChecklistSerializer, ChecklistItemSerializer
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

class VisaRequirementViewSet(ReadOnlyModelViewSet):
    queryset = VisaRequirement.objects.all()
    serializer_class = VisaRequirementSerializer

class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
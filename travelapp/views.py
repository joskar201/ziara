import django_filters
from rest_framework import generics
from .models import UserProfile, Destination
from .filters import UserProfileFilter, DestinationFilter
from .serializers import UserProfileSerializer, DestinationSerializer


class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = UserProfileFilter


class DestinationList(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = DestinationFilter

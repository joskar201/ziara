import django_filters
from .models import UserProfile, Destination


class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            'user_type': ['exact'],
            'phone_number': ['exact', 'icontains'],
            'bio': ['icontains'],
        }


class DestinationFilter(django_filters.FilterSet):
    class Meta:
        model = Destination
        fields = {
            'destination_type': ['exact'],
            'name': ['icontains'],
            'location': ['icontains'],
        }


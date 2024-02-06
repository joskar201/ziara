from django.urls import path
from . import views

urlpatterns = [
    # Endpoint for user profiles
    path('user-profiles/', views.UserProfileList.as_view(), name='user-profile-list'),

    # Endpoint for destinations
    path('destinations/', views.DestinationList.as_view(), name='destination-list'),
]

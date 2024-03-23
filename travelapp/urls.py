from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    DestinationViewSet, UserProfileViewSet, ActivityViewSet, 
    BookingViewSet, ItineraryViewSet, ItineraryItemViewSet, 
    UserRegistrationView, VisaRequirementViewSet, ChecklistViewSet, 
    ChecklistItemViewSet,TransferViewSet
    )


router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'itineraries', ItineraryViewSet)
router.register(r'itineraryitems', ItineraryItemViewSet)
router.register(r'visa-requirements', VisaRequirementViewSet)
router.register(r'checklists', ChecklistViewSet)
router.register(r'checklist-items', ChecklistItemViewSet)
router.register(r'transfers', TransferViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
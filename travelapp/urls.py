from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DestinationViewSet, UserProfileViewSet, ActivityViewSet,
    BookingViewSet, ItineraryViewSet, ItineraryItemViewSet,
    UserRegistrationView, VisaRequirementViewSet, ChecklistViewSet,
    ChecklistItemViewSet, TransferViewSet
)

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destinations')
router.register(r'userprofiles', UserProfileViewSet, basename='userprofiles')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'itineraries', ItineraryViewSet, basename='itineraries')
router.register(r'itineraryitems', ItineraryItemViewSet, basename='itineraryitems')
router.register(r'visa-requirements', VisaRequirementViewSet, basename='visa-requirements')
router.register(r'checklists', ChecklistViewSet, basename='checklists')
router.register(r'checklist-items', ChecklistItemViewSet, basename='checklist-items')
router.register(r'transfers', TransferViewSet, basename='transfers')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import (
    UserProfile, Destination, Activity, Booking, 
    Itinerary, ItineraryItem, VisaRequirement, 
    Checklist, ChecklistItem, Transfer
    )


class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse('user-registration')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "travel_preferences": "Mountains",
            "booking_history": "None"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)  # Ensure the response includes the user ID

class DestinationTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)  # Authenticate the test client

    def test_create_destination(self):
        url = reverse('destination-list')
        data = {
            "name": "Paris",
            "description": "City of Light",
            "location": "France",
            "destination_type": "cultural",
            "popular_activities": "Visiting museums",
            # Handle 'image' appropriately
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserProfileViewSetTest(APITestCase):
    def setUp(self):
        # Create a user and profile to test with
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user, bio='A simple bio', phone_number='123456789')
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profiles(self):
        url = reverse('userprofile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming this is the only profile


class ActivityViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)
        self.destination = Destination.objects.create(
            name="Test Destination", description="Test Description", location="Test Location",
            destination_type="adventure", popular_activities="Hiking, Swimming")
        self.activity = Activity.objects.create(
            name="Test Activity", description="Activity Description", activity_type="adventure",
            duration="2 hours", price="50.00", destination=self.destination)

    def test_create_activity(self):
        url = reverse('activity-list')
        data = {
            "name": "New Test Activity",
            "description": "New Activity Description",
            "activity_type": "leisure",
            "duration": "1 hour",
            "price": "20.00",
            "destination": self.destination.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_activities(self):
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one activity in setUp

class BookingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, bio="Test Bio")
        self.destination = Destination.objects.create(name="Test Destination", description="Description", location="Test Location", destination_type="Adventure")
        self.booking = Booking.objects.create(user_profile=self.user_profile, booking_type='hotel', booking_date='2023-01-01', start_date='2023-01-05', end_date='2023-01-10', details='Booking Details', price=200.00, is_confirmed=True)

    def test_create_booking(self):
        url = reverse('booking-list')
        data = {
            "user_profile": self.user_profile.id,
            "booking_type": "activity",
            "booking_date": "2023-01-02",
            "start_date": "2023-01-06",
            "end_date": "2023-01-11",
            "details": "New Booking Details",
            "price": 150.00,
            "is_confirmed": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_bookings(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming setUp created only one booking


class ItineraryViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.itinerary = Itinerary.objects.create(title="My Itinerary", user_profile=self.user.userprofile)
        self.itinerary_item = ItineraryItem.objects.create(itinerary=self.itinerary, description="Visit the Eiffel Tower")

    def test_itinerary_list_includes_items(self):
        url = reverse('itinerary-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('items' in response.data[0])
        self.assertEqual(len(response.data[0]['items']), 1)  # Checking if the items are included in the response

    # Add tests for create, update, delete as per your implementation

class ItineraryItemViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.itinerary = Itinerary.objects.create(title='Test Itinerary', user_profile=self.user.userprofile)
        self.itinerary_item = ItineraryItem.objects.create(itinerary=self.itinerary, description='Item 1')

    def test_create_itinerary_item(self):
        url = reverse('itineraryitem-list')
        data = {'itinerary': self.itinerary.id, 'description': 'Visit museum'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItineraryItem.objects.count(), 2)
        self.assertEqual(ItineraryItem.objects.last().description, 'Visit museum')

    def test_update_itinerary_item(self):
        url = reverse('itineraryitem-detail', kwargs={'pk': self.itinerary_item.pk})
        data = {'description': 'Updated Item'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.itinerary_item.refresh_from_db()
        self.assertEqual(self.itinerary_item.description, 'Updated Item')

    def test_delete_itinerary_item(self):
        url = reverse('itineraryitem-detail', kwargs={'pk': self.itinerary_item.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ItineraryItem.objects.count(), 0)

class VisaRequirementViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.destination = Destination.objects.create(name="Test Country", description="Beautiful place", location="Earth", destination_type="adventure")
        self.visa_requirement = VisaRequirement.objects.create(destination=self.destination, document_requirements="Passport", processing_time="5 days", fees=50.00)

    def test_list_visa_requirements(self):
        url = reverse('visarequirement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assumes only one visa requirement exists

    def test_retrieve_visa_requirement(self):
        url = reverse('visarequirement-detail', kwargs={'pk': self.visa_requirement.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['document_requirements'], 'Passport')

class ChecklistViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, bio="Test Bio")
        self.checklist = Checklist.objects.create(title="My Checklist", user=self.user)

    def test_create_checklist(self):
        url = reverse('checklist-list')
        data = {'title': 'New Checklist', 'user': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Checklist.objects.count(), 2)  # Assuming the setUp created one checklist already

    def test_list_checklists(self):
        url = reverse('checklist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming setUp created only one checklist

    # Include additional tests for update and delete functionalities if your API supports them

class ChecklistItemViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.checklist = Checklist.objects.create(title="Travel Checklist", user=self.user)
        self.checklist_item = ChecklistItem.objects.create(checklist=self.checklist, item_text="Passport", status="not_started")

    def test_create_checklist_item(self):
        url = reverse('checklistitem-list')
        data = {'checklist': self.checklist.id, 'item_text': "Visa", 'status': "not_started"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChecklistItem.objects.count(), 2)  # Assuming the setUp created one checklist item already

    def test_list_checklist_items(self):
        url = reverse('checklistitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming setUp created only one checklist item

    # Add tests for update and delete functionalities
    
class TransferViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.transfer = Transfer.objects.create(
            user=self.user,
            pickup_location="Airport",
            dropoff_location="Hotel",
            transfer_date="2023-01-01",
            transfer_time="12:00",
            number_of_passengers=2,
            vehicle_type="Sedan",
            special_requests="Child seat"
        )

    def test_create_transfer(self):
        url = reverse('transfer-list')
        data = {
            "user": self.user.id,
            "pickup_location": "Hotel",
            "dropoff_location": "Airport",
            "transfer_date": "2023-01-02",
            "transfer_time": "15:00",
            "number_of_passengers": 1,
            "vehicle_type": "Compact",
            "special_requests": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transfer.objects.count(), 2)

    def test_list_transfers(self):
        url = reverse('transfer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Implement similar tests for update and delete operations
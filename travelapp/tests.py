from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import UserProfile, Destination, Activity, Booking



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

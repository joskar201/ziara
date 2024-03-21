from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.conf import settings


class UserProfile(models.Model):
    # Link to Django's built-in user model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Additional fields
    user_type = models.CharField(max_length=30, choices=[
        ('adventure_explorer', 'Adventure Explorer'),
        ('family_vacationer', 'Family Vacationer'),
        ('business_traveler', 'Business Traveler'),
        ('travel_agent', 'Travel Agent'),
    ])
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Destination(models.Model):
    AMENITIES_CHOICES = [
        ('television', 'Television'),
        ('wifi', 'WiFi'),
        ('free_parking', 'Free Parking'),
        # Add more amenities as needed
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    destination_type = models.CharField(max_length=50, choices=[
        ('adventure', 'Adventure'),
        ('family', 'Family'),
        ('business', 'Business'),
        ('cultural', 'Cultural'),
        ('leisure', 'Leisure'),
    ])
    popular_activities = models.TextField()
    image = models.ImageField(upload_to='destination_images/', null=True, blank=True)
    amenities = models.JSONField(default=list)  # Stores list of amenities
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
    

class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    description = models.TextField()
    activity_type = models.CharField(max_length=50, choices=[
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('leisure', 'Leisure'),
        ('sport', 'Sport'),
        ('educational', 'Educational'),
    ])
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_adult = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_child = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.CharField(max_length=255, blank=True) 
    image = models.ImageField(upload_to='activity_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name}"
    

class Booking(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=50, choices=[
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
        ('activity', 'Activity'),
        ('transfer', 'Transfer'),
    ])
    booking_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.booking_type} - {self.start_date.strftime('%Y-%m-%d')}"
    

class Itinerary(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user_profile.user.username}"

class ItineraryItem(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='items')
    date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True, related_name='itinerary_items')
    type = models.CharField(max_length=50, choices=[
        ('flight', 'Flight'),
        ('accommodation', 'Accommodation'),
        ('activity', 'Activity'),
        ('transfer', 'Transfer'),
        ('other', 'Other'),
    ])

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.description}"


class CustomUser(AbstractUser):
    # Add additional fields here
    travel_preferences = models.TextField()
    booking_history = models.TextField()


class VisaRequirement(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='visa_requirements')
    document_requirements = models.TextField()
    processing_time = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    additional_notes = models.TextField(blank=True, null=True)


class Checklist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='checklists')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChecklistItem(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    item_text = models.CharField(max_length=255)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='not_started')

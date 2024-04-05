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
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    popular_activities = models.TextField()
    type = models.CharField(max_length=50, choices=[('city', 'City'), ('country', 'Country'), ('region', 'Region')])

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accommodations')
    amenities = models.ManyToManyField(Amenity, related_name='accommodations', blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    amenities = models.JSONField(default=list)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)    

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
    BOOKING_TYPES = [
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
        ('activity', 'Activity'),
        ('transfer', 'Transfer'),
        ('destination', 'Destination'),  # Assuming direct destination booking is possible
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=50, choices=BOOKING_TYPES)
    booking_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)

    # Optional ForeignKey to Activity
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')

    # Optional ForeignKey to Destination
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')

    # Optional ForeignKey to other types can be added similarly

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.booking_type} - {self.start_date.strftime('%Y-%m-%d')}"
    

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

class VisaRequirement(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='visa_requirements')
    document_requirements = models.TextField()
    processing_time = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    additional_notes = models.TextField(blank=True, null=True)


class Checklist(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='checklists')
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

class Transfer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transfers')
    booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    passengers = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=50, choices=(('Standard', 'Standard'), ('Luxury', 'Luxury')))
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transfer for {self.user.username} from {self.pickup_location} to {self.dropoff_location} on {self.pickup_time.strftime('%Y-%m-%d %H:%M')}" 
    
class Flight(models.Model):
    flight_number = models.CharField(max_length=255)
    departure_airport = models.CharField(max_length=255)
    arrival_airport = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='flights')

    def __str__(self):
        return f"{self.flight_number} from {self.departure_airport} to {self.arrival_airport}"
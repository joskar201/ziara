from django.db import models
from travelapp.models import UserProfile, Booking


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
from django.db import models
from travelapp.models import UserProfile, Booking


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
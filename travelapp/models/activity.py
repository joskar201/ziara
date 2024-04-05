from travelapp.models import UserProfile, Booking
from django.db import models


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
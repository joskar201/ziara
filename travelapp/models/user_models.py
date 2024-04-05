from django.db import models
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
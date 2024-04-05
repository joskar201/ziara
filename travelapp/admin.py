from django.contrib import admin
from .models import (
    Destination, Activity, Booking, Itinerary, 
    ItineraryItem, VisaRequirement, Checklist, ChecklistItem,
    Transfer
)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'activity_type', 'price')
    list_filter = ('activity_type', 'destination')
    search_fields = ('name', 'description', 'destination__name')

admin.site.register(Activity, ActivityAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'booking_type', 'booking_date', 'start_date', 'end_date', 'price', 'is_confirmed')
    list_filter = ('booking_type', 'is_confirmed', 'user_profile__user_type')
    search_fields = ('user_profile__user__username', 'details', 'booking_type')

admin.site.register(Booking, BookingAdmin)

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1

class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_profile', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'user_profile')
    search_fields = ('title', 'description', 'user_profile__user__username')
    inlines = [ItineraryItemInline]

admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(ItineraryItem)

class VisaRequirementAdmin(admin.ModelAdmin):
    list_display = ('destination', 'processing_time', 'fees')
    search_fields = ('destination__name',)
    list_filter = ('destination',)

admin.site.register(VisaRequirement, VisaRequirementAdmin)

class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1  # Adjust the number of empty forms displayed

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_profile', 'created_at')
    list_filter = ('created_at', 'user_profile')
    search_fields = ('title', 'user_profile__user__username')
    inlines = [ChecklistItemInline]  # This line includes ChecklistItemInline in the ChecklistAdmin

admin.site.register(Checklist, ChecklistAdmin)

class TransferAdmin(admin.ModelAdmin):
    list_display = ('pickup_location', 'dropoff_location', 'pickup_time', 'passengers', 'vehicle_type', 'user_profile_str')
    list_filter = ('pickup_time', 'vehicle_type', 'user_profile__user__username')
    search_fields = ('pickup_location', 'dropoff_location', 'user_profile__user__username')
    
    def user_profile_str(self, obj):
        return obj.user_profile.user.username
    user_profile_str.short_description = 'User'

admin.site.register(Transfer, TransferAdmin)

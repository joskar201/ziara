from django.contrib import admin

from .models import UserProfile, Destination, Activity, Booking, Itinerary, ItineraryItem

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'bio')
    search_fields = ('user__username', 'user_type', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'destination_type')
    search_fields = ('name', 'location', 'destination_type')
    list_filter = ('destination_type',)

admin.site.register(Destination, DestinationAdmin)

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

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from travelapp.models import (
    UserProfile, Destination, Activity, Booking, 
    Itinerary, ItineraryItem, 
    VisaRequirement, Checklist, ChecklistItem, Transfer
)

User = get_user_model()
faker = Faker()

class Command(BaseCommand):
    help = "Generates fake data for the app"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int, help='Number of fake users to create')

    def handle(self, *args, **options):
        users = options['users'] if options['users'] else 10  # Default to 10 users if not specified

        # Creating users and user profiles
        for _ in range(users):
            user = User.objects.create_user(username=faker.user_name(), email=faker.email(), password="password")
            user_type_choices = UserProfile._meta.get_field('user_type').choices

            UserProfile.objects.create(
                user=user,
                user_type=faker.random_element(elements=[choice[0] for choice in user_type_choices]),
                phone_number=faker.phone_number(),
                bio=faker.text(),
                profile_pic=faker.image_url()
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully added {users} fake users and related data.'))
        
        # Creating destinations
        destination_types = ['adventure', 'family', 'business', 'cultural', 'leisure']
        amenities_choices = ['television', 'wifi', 'free_parking']  # Example amenities

        for _ in range(10):
            Destination.objects.create(
                name=faker.city(),
                description=faker.text(max_nb_chars=200),
                location=f"{faker.city()}, {faker.country()}",
                destination_type=faker.random_element(elements=destination_types),
                popular_activities=faker.sentence(nb_words=6),
                amenities=faker.random_elements(elements=amenities_choices, unique=True, length=faker.random_int(min=1, max=len(amenities_choices))),
                price_per_night=faker.pydecimal(left_digits=4, right_digits=2, positive=True),
                # Assume 'image' field handled elsewhere or not required for seed data
            )

        self.stdout.write(self.style.SUCCESS('Successfully added fake destinations.'))

        # Creating activities
        activity_types = ['adventure', 'cultural', 'leisure', 'sport', 'educational']

        for destination in Destination.objects.all():
            for _ in range(5):
                Activity.objects.create(
                    destination=destination,
                    name=f'{faker.word().capitalize()} {faker.random_element(elements=activity_types)}',
                    description=faker.paragraph(nb_sentences=3),
                    activity_type=faker.random_element(elements=activity_types),
                    duration=f"{faker.random_int(min=1, max=5)} hours",
                    price=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                    location=faker.city(),
                    # Assume 'image' field handled elsewhere or not required for seed data
                    price_per_adult=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                    price_per_child=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                )

        self.stdout.write(self.style.SUCCESS('Successfully added fake activities.'))

        # Creating visa requirements
        for destination in Destination.objects.all():
            VisaRequirement.objects.create(
                destination=destination,
                document_requirements=faker.text(max_nb_chars=100),
                processing_time=f"{faker.random_int(min=1, max=15)} days",
                fees=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
                additional_notes=faker.sentence(nb_words=15),
            )

        self.stdout.write(self.style.SUCCESS('Successfully added fake visa requirements.'))

        # Creating checklists and checklist items
        for user_profile in UserProfile.objects.all():
            checklist = Checklist.objects.create(
                user_profile=user_profile,
                title=f'{faker.word().capitalize()} Checklist',
            )
            
            for _ in range(faker.random_int(min=3, max=10)):
                ChecklistItem.objects.create(
                    checklist=checklist,
                    item_text=faker.sentence(),
                    status=faker.random_element(elements=['not_started', 'in_progress', 'completed']),
                )

        self.stdout.write(self.style.SUCCESS('Successfully created checklists and checklist items.'))

        # Continuing vehicle types
        vehicle_types = ['Standard', 'Luxury']

        for user_profile in UserProfile.objects.all():
            # Assuming each user_profile might have multiple bookings, picking one for the transfer
            booking = Booking.objects.filter(user_profile=user_profile).order_by('?').first()

            Transfer.objects.create(
                user_profile=user_profile,
                booking=booking,
                pickup_location=faker.address(),
                dropoff_location=faker.address(),
                pickup_time=faker.date_time_between(start_date="+1d", end_date="+30d"),
                passengers=faker.random_int(min=1, max=6),
                vehicle_type=faker.random_element(elements=vehicle_types),
                special_requests=faker.sentence() if faker.boolean(chance_of_getting_true=25) else '',
            )

        self.stdout.write(self.style.SUCCESS('Successfully created transfers.'))

        # Creating itineraries and itinerary items
        for user_profile in UserProfile.objects.all():
            # Create a few itineraries for each user profile
            for _ in range(faker.random_int(min=1, max=3)):
                itinerary = Itinerary.objects.create(
                    user_profile=user_profile,
                    title=f"{faker.word().capitalize()} Itinerary",
                    start_date=faker.date_time_between(start_date="+1d", end_date="+10d"),
                    end_date=faker.date_time_between(start_date="+11d", end_date="+30d"),
                    description=faker.text(max_nb_chars=200),
                )

                # Create itinerary items for each itinerary
                for _ in range(faker.random_int(min=2, max=5)):
                    ItineraryItem.objects.create(
                        itinerary=itinerary,
                        date=faker.date_time_between(start_date=itinerary.start_date, end_date=itinerary.end_date),
                        description=faker.sentence(nb_words=6),
                        location=f"{faker.city()}, {faker.country()}",
                        # Assuming 'booking' is optional and only added if relevant
                        # Example: booking=Booking.objects.filter(user_profile=user_profile).order_by('?').first()
                        type=faker.random_element(elements=[
                            'flight', 'accommodation', 'activity', 'transfer', 'other'
                        ]),
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created itineraries and itinerary items.'))


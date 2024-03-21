from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from travelapp.models import UserProfile, Destination, Activity, Booking, Itinerary, ItineraryItem, VisaRequirement, Checklist, ChecklistItem,CustomUser

User = get_user_model()
faker = Faker()

class Command(BaseCommand):
    help = "Generates fake data for the app"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int, help='Number of fake users to create')

    def handle(self, *args, **options):
        users = options['users']

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

        # Similar approach for other models like Destination, Activity, etc.
        # Create Destination instances
        # Create Activity instances linked to Destinations
        # Create VisaRequirement instances linked to Destinations
        # Create Checklist and ChecklistItem instances linked to Users

        self.stdout.write(self.style.SUCCESS(f'Successfully added {users} fake users and related data.'))
        
        
        destination_types = ['adventure', 'family', 'business', 'cultural', 'leisure']
        amenities_choices = ['television', 'wifi', 'free_parking']  # Add more as per your model

        for _ in range(10):  # Adjust for the number of Destinations you want
            Destination.objects.create(
                name=faker.city(),
                description=faker.text(max_nb_chars=200),
                location=f"{faker.city()}, {faker.country()}",
                destination_type=faker.random_element(elements=destination_types),
                popular_activities=faker.sentence(nb_words=6),
                amenities=faker.random_elements(elements=amenities_choices, unique=True, length=faker.random_int(min=1, max=len(amenities_choices))),
                price_per_night=faker.pydecimal(left_digits=4, right_digits=2, positive=True),
                # Handle 'image' as per your requirements
            )

        self.stdout.write(self.style.SUCCESS('Successfully added fake destinations.'))



        activity_types = ['adventure', 'cultural', 'leisure', 'sport', 'educational']

        for destination in Destination.objects.all():
            for _ in range(5):  # Adjust for the desired number of activities per destination
                Activity.objects.create(
                    destination=destination,
                    name=f'{faker.word().capitalize()} {faker.random_element(elements=activity_types).capitalize()}',
                    description=faker.paragraph(nb_sentences=3),
                    activity_type=faker.random_choices(activity_types),
                    duration=f"{faker.random_int(min=1, max=5)} hours",
                    price=faker.pydecimal(left_digits=2, right_digits=2, positive=True),
                    # Handle the image field as per your requirements
                )

        self.stdout.write(self.style.SUCCESS('Successfully added fake activities.'))

        for destination in Destination.objects.all():
            VisaRequirement.objects.create(
                destination=destination,
                document_requirements=faker.text(max_nb_chars=100),
                processing_time=f"{faker.random_int(min=1, max=15)} days",
                fees=faker.pydecimal(left_digits=3, right_digits=2, positive=True),
                additional_notes=faker.sentence(nb_words=15),
            )

        self.stdout.write(self.style.SUCCESS('Successfully added fake visa requirements.'))


        checklist_status_choices = ['not_started', 'in_progress', 'completed']

        # Assuming CustomUser is your user model
        for user in CustomUser.objects.all():
            # Create a checklist for each user
            checklist = Checklist.objects.create(
                user=user,
                title=f'{faker.word().capitalize()} Checklist',
                # Add any other fields as necessary
            )
            
            # Create checklist items for each checklist
            for _ in range(faker.random_int(min=3, max=10)):  # Random number of items
                ChecklistItem.objects.create(
                    checklist=checklist,
                    item_text=faker.sentence(),
                    status=faker.random_element(elements=checklist_status_choices),
                    # Add any other fields as necessary
                )

        self.stdout.write(self.style.SUCCESS('Successfully created checklists and checklist items.'))






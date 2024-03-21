from django.core.management.base import BaseCommand
from faker import Faker
from models import CustomUser, Checklist

class Command(BaseCommand):
    help = 'Generates fake data for your app'

    def handle(self, *args, **options):
        faker = Faker()

        # Example: Create 10 fake users
        for _ in range(10):
            CustomUser.objects.create(
                username=faker.user_name(),
                email=faker.email(),
                # Set other fields or handle them as required
            )

        # Example: Create fake checklists for each user
        for user in CustomUser.objects.all():
            Checklist.objects.create(
                title=faker.sentence(),
                user=user,
                # Fill in additional fields
            )

        self.stdout.write(self.style.SUCCESS('Successfully created fake data'))

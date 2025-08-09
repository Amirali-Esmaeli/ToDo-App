from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import User
from todo.models import Task


class Command(BaseCommand):
    help = "inserting dummy data"

    def handle(self, *args, **options):
        fake = Faker()
        user = User.objects.create_user(
            email=fake.email(), password="Test@123456"
        )

        for _ in range(5):
            Task.objects.create(
                user=user,
                title=fake.text(max_nb_chars=15),
                complete=random.choice([True, False]),
            )

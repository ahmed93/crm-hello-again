import random
import time

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from app.models import Address, AppUser, CustomerRelationship

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("--target", type=int, default=100_000)
        parser.add_argument("--batch", type=int, default=5_000)

    def handle(self, *args, **options):
        target = options["target"]
        batch = options["batch"]
        self.stdout.write(f"Seeding {target} records (batch={batch})...")
        start_time = time.time()
        created = 0

        while created < target:
            this_batch = min(batch, target - created)
            now = timezone.now()
            addresses = [
                Address(
                    street=fake.street_name(),
                    street_number=str(random.randint(1, 9999)),
                    city_code=str(random.randint(1000, 99999)),
                    city=fake.city(),
                    country="AT",
                )
                for _ in range(this_batch)
            ]

            with transaction.atomic():
                Address.objects.bulk_create(addresses, batch_size=1000)
                address_ids = list(
                    Address.objects.values_list("id", flat=True).order_by("-id")[
                        :this_batch
                    ]
                )
                address_ids.reverse()
                users = [
                    AppUser(
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        gender=random.choice(["M", "F", "O"]),
                        customer_id=fake.uuid4(),
                        phone_number=fake.phone_number(),
                        address_id=addr_id,
                        birthday=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    )
                    for addr_id in address_ids
                ]
                AppUser.objects.bulk_create(users, batch_size=1000)
                user_ids = list(
                    AppUser.objects.values_list("id", flat=True).order_by("-id")[
                        :this_batch
                    ]
                )
                user_ids.reverse()
                relationships = [
                    CustomerRelationship(
                        appuser_id=u_id,
                        points=random.randint(0, 10000),
                        last_activity=now,
                    )
                    for u_id in user_ids
                ]
                CustomerRelationship.objects.bulk_create(relationships, batch_size=1000)
            created += this_batch
            self.stdout.write(f"Inserted batch {this_batch} (total {created}/{target})")
        total_time = time.time() - start_time
        self.stdout.write(
            f"Seeding completed in {total_time:.2f}s for {target} records."
        )

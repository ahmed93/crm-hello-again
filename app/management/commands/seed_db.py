import random
import time
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from app.models import Address, AppUser, CustomerRelationship

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("--target", type=int, default=100000)
        parser.add_argument("--batch", type=int, default=5000)
        parser.add_argument("--start-id", type=int, default=1)

    def handle(self, *args, **options):
        target = options["target"]
        batch = options["batch"]
        start_id = options["start_id"]

        self.stdout.write(f"Seeding target={target} batch={batch} start_id={start_id}")
        created = 0
        start_time = time.time()

        while created < target:
            this_batch = min(batch, target - created)
            t0 = time.time()

            addresses = []
            for i in range(this_batch):
                addresses.append(
                    Address(
                        street=fake.street_name(),
                        street_number=str(random.randint(1, 9999)),
                        city_code=str(random.randint(1000, 99999)),
                        city=fake.city(),
                        country=fake.country_code(),
                    )
                )
            with transaction.atomic():
                Address.objects.bulk_create(addresses, batch_size=1000)

            recent_addresses = list(Address.objects.order_by("-id")[:this_batch])
            recent_addresses.reverse()

            users = []
            for addr in recent_addresses:
                fn = fake.first_name()
                ln = fake.last_name()
                users.append(
                    AppUser(
                        first_name=fn,
                        last_name=ln,
                        gender=random.choice(["M", "F", "O"]),
                        customer_id=str(fake.uuid4()),
                        phone_number=fake.phone_number(),
                        address=addr,
                        birthday=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    )
                )
            with transaction.atomic():
                AppUser.objects.bulk_create(users, batch_size=1000)

            recent_users = list(AppUser.objects.order_by("-id")[:this_batch])
            recent_users.reverse()

            relationships = []
            now = timezone.now()
            for u in recent_users:
                relationships.append(
                    CustomerRelationship(
                        appuser=u, points=random.randint(0, 10000), last_activity=now
                    )
                )
            with transaction.atomic():
                CustomerRelationship.objects.bulk_create(relationships, batch_size=1000)

            created += this_batch
            t1 = time.time()
            self.stdout.write(
                f"Inserted batch {this_batch} (total {created}/{target}) in {t1 - t0:.2f}s"
            )

        total_time = time.time() - start_time
        self.stdout.write(
            f"Seeding finished. Inserted {created} rows for each table in {total_time:.2f}s"
        )

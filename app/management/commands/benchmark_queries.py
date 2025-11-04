import time

from django.core.management.base import BaseCommand
from django.db import connection, reset_queries

from app.models import AppUser


class Command(BaseCommand):
    help = "Benchmark performance"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=5000)
        parser.add_argument("--repeats", type=int, default=5)

    def timed_query(self, qs, repeats=5):
        durations = []
        for _ in range(repeats):
            reset_queries()
            start = time.time()
            if qs._prefetch_related_lookups:
                list(qs)
            else:
                list(qs.iterator(chunk_size=2000))
            durations.append(time.time() - start)

        avg_duration = sum(durations) / repeats
        query_count = len(connection.queries)
        return avg_duration, query_count

    def handle(self, *args, **options):
        limit = options["limit"]
        repeats = options["repeats"]

        print(f"\nRunning ORM benchmark for {limit} users ({repeats}× repeats)...\n")

        tests = [
            (
                "join",
                AppUser.objects.select_related("address").prefetch_related(
                    "relationship"
                )[:limit],
                AppUser.objects.all()[:limit],
            ),
            (
                "filter",
                AppUser.objects.filter(gender="M")[:limit],
                AppUser.objects.filter(gender="M")[:limit],
            ),
            (
                "order",
                AppUser.objects.order_by("last_name")[:limit],
                AppUser.objects.order_by("last_name")[:limit],
            ),
            (
                "paginate",
                AppUser.objects.all()[1000:2000],
                AppUser.objects.all()[1000:2000],
            ),
        ]

        for name, opt_qs, plain_qs in tests:
            opt_time, opt_q = self.timed_query(opt_qs, repeats)
            plain_time, plain_q = self.timed_query(plain_qs, repeats)
            diff = plain_time - opt_time
            match diff:
                case d if d > 0:
                    state = "faster"
                case d if d < 0:
                    state = "slower"
                case _:
                    state = "-"
            print(
                f"{name.title():<10}: "
                f"opt={opt_time:.3f}s ({opt_q}q), "
                f"plain={plain_time:.3f}s ({plain_q}q), "
                f"Δ={abs(diff):.3f}s {state}"
            )

        print("\nBenchmark completed.\n")

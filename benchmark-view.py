import datetime
import os
import time
from statistics import mean

import requests

BASE_URL = os.getenv("BENCH_URL", "http://localhost:8000/api/")
REPEATS = 5
OUTPUT_DIR = ".benchmark"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEST_ENDPOINTS = [
    ("All Users (paginated)", "users/"),
    ("Filter by name", "users/?first_name=Anna"),
    ("Filter by city", "users/?address__city=Vienna"),
    ("Filter by postal code", "users/?address__city_code=1010"),
    ("Filter by points", "users/?relationship__points__gte=100"),
    ("Sort by name", "users/?ordering=first_name"),
    ("Sort by created desc", "users/?ordering=-created"),
    ("Search 'John'", "users/?search=John"),
    ("Custom pagination", "users/?page=2&page_size=100"),
    ("Recent relationships", "relationships/?ordering=-last_activity"),
    ("Addresses by city", "addresses/?city=Graz"),
]


def timed_request(url: str, repeats: int):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        try:
            response = requests.get(url, timeout=10)
            elapsed = time.perf_counter() - start
            if response.status_code == 200:
                times.append(elapsed)
            else:
                print(f"{url} returned {response.status_code}")
        except requests.RequestException as e:
            print(f"Request error on {url}: {e}")
    return mean(times) if times else None


def run_view_benchmarks():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"view_benchmark_{timestamp}.log")
    print(f"Running HTTP view benchmarks ({REPEATS}× repeats)...\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Running HTTP view benchmarks ({REPEATS}× repeats)...\n\n")
        for name, path in TEST_ENDPOINTS:
            url = BASE_URL.rstrip("/") + "/" + path.lstrip("/")
            avg_time = timed_request(url, REPEATS)
            if avg_time is not None:
                line = f"{name:<35}: {avg_time:.3f}s avg"
            else:
                line = f"{name:<35}: failed"
            print(line)
            f.write(line + "\n")
        f.write("\nBenchmark complete.\n")
    print(f"\nBenchmark complete. Results saved to {output_file}")


if __name__ == "__main__":
    run_view_benchmarks()

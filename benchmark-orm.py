import datetime
import os
import subprocess

BENCHMARKS = ["bench-5k", "bench-10k", "bench-50k", "bench-500k", "bench-1M"]

OUTPUT_DIR = ".benchmark"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(OUTPUT_DIR, f"benchmark_{timestamp}.log")

with open(output_path, "w") as outfile:
    outfile.write(f"=== Django ORM Benchmark Report ({timestamp}) ===\n\n")

    for command in BENCHMARKS:
        cmd = ["make", command]

        outfile.write(f"Running {command} \n")
        outfile.flush()

        print(f"▶️ Running Benchmark for '{command}'")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            outfile.write(result.stdout)
        except subprocess.CalledProcessError as e:
            outfile.write(f"[ERROR] {command} failed:\n{e.stderr}\n")

        outfile.write("\n" + "=" * 80 + "\n\n")
        outfile.flush()

print(f"✅ All benchmarks completed.\nResults saved to: {output_path}")

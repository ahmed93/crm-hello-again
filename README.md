# CRM-Task API Benchmark Results

## ⚙️ Installation

To run the project and reproduce the benchmarks locally:

1. **Install Docker** and **Docker Compose**
   Ensure both are available in your terminal:

   ```bash
   docker --version
   docker compose version
   ```

2. **Clone the repository**

   ```bash
   git clone https://github.com/<your-org>/CRM-Task.git
   cd CRM-Task
   ```

3. **Start all services**
   Build and launch the full stack (backend, DB, Redis):

   ```bash
   make deploy
   ```

4. **Apply database migrations**

   ```bash
   make db:migrate
   ```

5. **Run the benchmark**
   Once the backend is running at `http://localhost:8000/`:

   ```bash
   python benchmark-view.py
   ```

6. **View results**
   Results are stored under:

   ```
   .output/view_benchmark_<timestamp>.log
   ```

---

## 📈 Benchmark Results

### With Redis Caching

| Test | Avg Time |
|------|-----------|
| All Users (paginated) | **0.021s** |
| Filter by name | **0.010s** |
| Filter by city | **0.013s** |
| Filter by postal code | **0.015s** |
| Filter by points | **0.014s** |
| Sort by name | **0.014s** |
| Sort by created desc | **0.014s** |
| Search “John” | **0.056s** |
| Custom pagination | **0.014s** |
| Recent relationships | **0.009s** |
| Addresses by city | **0.010s** |

---

### Without Redis Caching

| Test | Avg Time |
|------|-----------|
| All Users (paginated) | 0.065s |
| Filter by name | 0.035s |
| Filter by city | 0.058s |
| Filter by postal code | 0.060s |
| Filter by points | 0.060s |
| Sort by name | 0.059s |
| Sort by created desc | 0.060s |
| Search “John” | 0.253s |
| Custom pagination | 0.059s |
| Recent relationships | 0.038s |
| Addresses by city | 0.030s |

**Average speedup:** ~3–4× with Redis enabled.

---

## 🔗 Clickable Test URLs

| Description | Example URL |
|--------------|-------------|
| **Filter by City (Alias)** | [http://localhost:8000/api/users/?city=Kylemouth](http://localhost:8000/api/users/?city=Kylemouth) |
| **Filter by Country** | [http://localhost:8000/api/users/?address__country=AT](http://localhost:8000/api/users/?address__country=AT) |
| **Filter by Points (>100)** | [http://localhost:8000/api/users/?relationship__points__gte=100](http://localhost:8000/api/users/?relationship__points__gte=100) |
| **Filter by Birthday (>= 1990)** | [http://localhost:8000/api/users/?birthday__gte=1990-01-01](http://localhost:8000/api/users/?birthday__gte=1990-01-01) |
| **Sort by Birthday** | [http://localhost:8000/api/users/?ordering=birthday](http://localhost:8000/api/users/?ordering=birthday) |
| **Sort by Last Activity** | [http://localhost:8000/api/users/?ordering=-relationship__last_activity](http://localhost:8000/api/users/?ordering=-relationship__last_activity) |
| **Search (Name/Phone)** | [http://localhost:8000/api/users/?search=John](http://localhost:8000/api/users/?search=John) |
| **Advanced: City + Points** | [http://localhost:8000/api/users/?city=Kylemouth&relationship__points__gte=500](http://localhost:8000/api/users/?city=Kylemouth&relationship__points__gte=500) |

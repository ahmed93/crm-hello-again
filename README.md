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
   python run_viewBenchmark.py
   ```

6. **View results**
   Results are stored under:

   ```
   .output/view_benchmark_<timestamp>.log
   ```

---

## ⚙️ Routes

Your available endpoints:

| Endpoint | Description |
|-----------|-------------|
| [`/users/`](http://localhost:8000/api/users/) | List, filter, order, and search users |
| [`/addresses/`](http://localhost:8000/api/addresses/) | List or filter addresses |
| [`/relationships/`](http://localhost:8000/api/relationships/) | Customer relationships |

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
| All users (paginated) | [http://localhost:8000/api/users/?page=1&page_size=50](http://localhost:8000/api/users/?page=1&page_size=50) |
| Filter by name | [http://localhost:8000/api/users/?first_name=John](http://localhost:8000/api/users/?first_name=John) |
| Filter by city | [http://localhost:8000/api/addresses/?city=Vienna](http://localhost:8000/api/addresses/?city=Vienna) |
| Filter by postal code | [http://localhost:8000/api/addresses/?city_code=1010](http://localhost:8000/api/addresses/?city_code=1010) |
| Filter by points | [http://localhost:8000/api/relationships/?ordering=points](http://localhost:8000/api/relationships/?ordering=points) |
| Sort by name | [http://localhost:8000/api/users/?ordering=last_name](http://localhost:8000/api/users/?ordering=last_name) |
| Sort by created desc | [http://localhost:8000/api/users/?ordering=-created](http://localhost:8000/api/users/?ordering=-created) |
| Search “John” | [http://localhost:8000/api/users/?search=John](http://localhost:8000/api/users/?search=John) |
| Custom pagination | [http://localhost:8000/api/users/?page=10&page_size=50](http://localhost:8000/api/users/?page=10&page_size=50) |
| Recent relationships | [http://localhost:8000/api/relationships/?ordering=-last_activity](http://localhost:8000/api/relationships/?ordering=-last_activity) |
| Addresses by city | [http://localhost:8000/api/addresses/?city=Vienna](http://localhost:8000/api/addresses/?city=Vienna) |

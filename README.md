# CRM-Task API Benchmark Results

This document summarizes API performance benchmarks for the CRM backend project, comparing response times **with** and **without Redis caching**.

---

## ⚙️ Routes

Your available endpoints:

| Endpoint | Description |
|-----------|-------------|
| [`/users/`](http://localhost:8000/users/) | List, filter, order, and search users |
| [`/addresses/`](http://localhost:8000/addresses/) | List or filter addresses |
| [`/relationships/`](http://localhost:8000/relationships/) | Customer relationships |

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
| All users (paginated) | [http://localhost:8000/users/?page=1&page_size=50](http://localhost:8000/users/?page=1&page_size=50) |
| Filter by name | [http://localhost:8000/users/?first_name=John](http://localhost:8000/users/?first_name=John) |
| Filter by city | [http://localhost:8000/addresses/?city=Vienna](http://localhost:8000/addresses/?city=Vienna) |
| Filter by postal code | [http://localhost:8000/addresses/?city_code=1010](http://localhost:8000/addresses/?city_code=1010) |
| Filter by points | [http://localhost:8000/relationships/?ordering=points](http://localhost:8000/relationships/?ordering=points) |
| Sort by name | [http://localhost:8000/users/?ordering=last_name](http://localhost:8000/users/?ordering=last_name) |
| Sort by created desc | [http://localhost:8000/users/?ordering=-created](http://localhost:8000/users/?ordering=-created) |
| Search “John” | [http://localhost:8000/users/?search=John](http://localhost:8000/users/?search=John) |
| Custom pagination | [http://localhost:8000/users/?page=10&page_size=50](http://localhost:8000/users/?page=10&page_size=50) |
| Recent relationships | [http://localhost:8000/relationships/?ordering=-last_activity](http://localhost:8000/relationships/?ordering=-last_activity) |
| Addresses by city | [http://localhost:8000/addresses/?city=Vienna](http://localhost:8000/addresses/?city=Vienna) |

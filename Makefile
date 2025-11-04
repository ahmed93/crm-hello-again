.PHONY:
	deploy
	db-migrate

deploy:
	docker compose up -d --build

db-shell:
	docker exec -it crm_web python manage.py dbshell

db-migrate:
	docker exec -it crm_web python manage.py makemigrations
	docker exec -it crm_web python manage.py migrate

db-seed-small:
	docker exec -it crm_web python manage.py seed_db --target 1000 --batch 250

db-seed:
	docker exec -it crm_web python manage.py seed_db --target 3000000 --batch 5000

bench-5k:
	docker exec -it crm_web python manage.py benchmark_queries --limit 5000

bench-10k:
	docker exec -it crm_web python manage.py benchmark_queries --limit 10000

bench-50k:
	docker exec -it crm_web python manage.py benchmark_queries --limit 50000

bench-100k:
	docker exec -it crm_web python manage.py benchmark_queries --limit 100000

bench-500k:
	docker exec -it crm_web python manage.py benchmark_queries --limit 500000

bench-1M:
	docker exec -it crm_web python manage.py benchmark_queries --limit 1000000

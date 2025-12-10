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

.PHONY: deploy

deploy:
	docker compose up -d --build

db-shell:
	docker exec -it crm_web python manage.py dbshell

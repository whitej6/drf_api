test:
	docker-compose run --rm app sh -c "./manage.py test && flake8"

makemigrations:
	docker-compose run --rm app sh -c "./manage.py makemigrations"

migrate:
	docker-compose run --rm app sh -c "./manage.py migrate"

up:
	docker-compose up

detached:
	docker-compose up -d
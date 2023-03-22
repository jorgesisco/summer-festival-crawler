install:
	pipenv install -r requirements.txt
	pipenv shell

run:
	docker-compose up

build:
	docker-compose build
	docker-compose up

down:
	docker-compose down


reset:
	docker-compose down
	docker-compose build
	docker-compose up -d
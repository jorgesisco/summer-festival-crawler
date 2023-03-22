install:
	pipenv install -r requirements.txt
	pipenv shell


freeze:
	pip3 freeze > requirements.txt

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
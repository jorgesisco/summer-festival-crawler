install:
	pipenv install -r requirements.txt
	pipenv shell


freeze:
	pip3 freeze > requirements.txt


build:
	 docker-compose up --build

delete:
	docker-compose down


reset:
	docker-compose down
	docker volume rm my_adminer_data
	docker-compose up -d


#docker exec -it summer-festivals-crawler-app  psql -U admin -d database
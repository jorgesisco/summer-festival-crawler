install:
	pipenv install -r requirements.txt
	pipenv shell


freeze:
	pip3 freeze > requirements.txt
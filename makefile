all: update run

build:
	docker compose build
	docker image prune -f
start:
	docker compose up -d
stop:
	docker compose down

scan:
	docker scan exam-python

deploy:
	git branch -D herokuStaging
	git branch herokuStaging
	git push -f heroku herokuStaging:main
create:
ifeq ("$(wildcard .venv)","")
	python3 -m venv .venv
endif
	source .venv/bin/activate
	python3 -m pip install --upgrade pip
update:
	set -a
	source .env
	set +a
	python3 -m pip freeze > requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
run:
	set -a
	source .env
	set +a
	python3 manage.py runserver 
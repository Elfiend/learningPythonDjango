all: update build start

build:
	docker compose build
start:
	docker compose up -d
stop:
	docker compose down

scan:
	docker scan exam-python

update:
	python3 -m pip freeze > pyexam/requirements.txt
	python3 pyexam/manage.py makemigrations
	python3 pyexam/manage.py migrate
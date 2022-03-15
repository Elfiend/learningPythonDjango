FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFRED=1
WORKDIR /code

COPY pyexam/requirements.txt /code/requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY pyexam/ /code/

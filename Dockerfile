FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

ARG DIRPATH=/app
WORKDIR ${DIRPATH}

COPY requirements.txt ${DIRPATH}
RUN python3 -m pip install -r requirements.txt

COPY . ${DIRPATH}
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD python3 manage.py runserver 0.0.0.0:8000
EXPOSE 8000
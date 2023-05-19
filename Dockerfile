FROM cheesecake87/pysupervisor:latest
WORKDIR /flask
RUN apk update && apk upgrade
# TIMEZONE
RUN apk add --no-cache tzdata
ENV TZ=Europe/London
# See here for timezones:
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
COPY app app
RUN mkdir "/flask/app/db"
COPY gunicorn.conf.py gunicorn.conf.py
COPY requirements.txt requirements.txt
COPY supervisor.apps.ini /pysupervisor/supervisor.apps.ini
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt

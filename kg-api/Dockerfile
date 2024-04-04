FROM python:3.8-slim

RUN apt-get -y update

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY ./src/ /app/
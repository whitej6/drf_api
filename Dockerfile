FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && \
    mkdir /app && \
    adduser -D ntc_user

WORKDIR /app

COPY ./app /app

USER ntc_user


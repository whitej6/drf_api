FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && \
    mkdir /app && \
    adduser -D ntc_user && \
    apk del .tmp-build-deps

WORKDIR /app

COPY ./app /app

USER ntc_user


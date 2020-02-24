FROM python:alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --update --no-cache postgresql-dev gcc libc-dev make python3-dev musl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . .

EXPOSE 8080

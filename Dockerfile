FROM python:3.8-slim-buster

RUN apt-get update && apt-get install --no-install-recommends -y \
                                      build-essential \
                                      python3-dev \
                                      libpq-dev \
                                      && apt-get clean \
                                      && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements/prod.txt /app/prod.txt
COPY requirements/base.txt /app/base.txt
RUN pip install -r prod.txt

COPY . /app
ENV PYTHONPATH=/app

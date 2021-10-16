FROM python:3.8-slim-buster

RUN apt-get update && apt-get install --no-install-recommends -y \
                                      build-essential \
                                      python3-dev \
                                      libpq-dev \
                                      && apt-get clean \
                                      && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

ARG ENVMODE=dev
ENV ENV_MODE=${ENVMODE}

RUN if [ "$ENVMODE" = "prod" ] ; then pip install -r requirements/prod.txt ; else pip install -r requirements/dev.txt ; fi

ENV PYTHONPATH=/app

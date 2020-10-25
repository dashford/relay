FROM library/python:3.9.0-alpine

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile Pipfile
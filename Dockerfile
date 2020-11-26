FROM library/python:3.6-alpine

WORKDIR /usr/src/app

VOLUME /usr/src/app/config

RUN pip install pipenv

COPY Pipfile Pipfile

RUN pipenv install --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "-u", "relay.py"]
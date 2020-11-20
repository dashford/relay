FROM library/python:3.6-alpine

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile Pipfile

RUN pipenv install --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "-u", "relay.py"]
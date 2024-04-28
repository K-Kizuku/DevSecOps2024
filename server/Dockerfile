FROM python:3.10.6

RUN mkdir -p /opt
COPY . /opt
WORKDIR /opt

RUN apt update
RUN apt install -y libpq-dev build-essential
RUN pip install pipenv
RUN pipenv install 
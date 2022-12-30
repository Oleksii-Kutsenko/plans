FROM python:3.11.0

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update \
    && apt install -y libpq-dev gcc python3-dev musl-dev g++

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements-dev.txt .
COPY ./requirements-tests.txt .
COPY ./requirements.txt .
RUN pip install -r requirements-tests.txt

# copy project
COPY . .

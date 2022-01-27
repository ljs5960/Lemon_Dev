# pull official base image
FROM python:3.8.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev
COPY . /usr/src/app/

# install dependencied
RUN pip install --upgrade pip
RUN pip instll -r requirements.txt
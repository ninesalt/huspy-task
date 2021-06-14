FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
EXPOSE 8000
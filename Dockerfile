FROM python:3.8.3-slim-buster
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY .env .
COPY ./src .
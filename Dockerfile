FROM python:3.9-slim AS production

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev 

COPY requirements/prod.txt ./requirements/prod.txt
RUN pip install -r ./requirements/prod.txt

COPY lime_website/manage.py ./lime_website/manage.py
COPY lime_website/setup.cfg ./lime_website/setup.cfg
COPY lime_website/lime_website ./lime_website/lime_website

EXPOSE 8000

FROM production AS development

COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install -r ./requirements/dev.txt

COPY . .

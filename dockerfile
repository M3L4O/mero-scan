# syntax=docker/dockerfile:1
FROM python:3.12-alpine
WORKDIR /work
RUN apk add --no-cache gcc musl-dev linux-headers
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
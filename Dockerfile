FROM python:3.9-slim

WORKDIR /weather

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

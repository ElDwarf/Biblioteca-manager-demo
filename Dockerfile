FROM python:3.9

WORKDIR /app/Biblioteca

COPY requirements.txt /app/Biblioteca

RUN pip install -r requirements.txt


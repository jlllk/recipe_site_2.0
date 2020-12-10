FROM python:3.8.3

WORKDIR /code

COPY requirements/prod.txt .
RUN pip install -r prod.txt

COPY . .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
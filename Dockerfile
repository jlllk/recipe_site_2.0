FROM python:3.8.3

WORKDIR /code

COPY requirements/requirements .
RUN pip install -r requirements/prod.txt

COPY . .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
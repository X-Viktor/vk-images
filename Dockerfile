FROM python:3.9.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY docker/django/uwsgi.ini ./uwsgi.ini
RUN mkdir -p /var/log/web/uwsgi && chown -R root:root /var/log/web/uwsgi

COPY . .

RUN chmod +x docker/django/entrypoint.sh

CMD ["docker/django/entrypoint.sh"]

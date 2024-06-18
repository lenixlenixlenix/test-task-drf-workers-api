FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /db.sqlite3

EXPOSE 8080

ENV TZ Europe/Moscow

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
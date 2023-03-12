FROM python:3.10

ENV PYTHONNUNBUFFERED 1

RUN mkdir /Twiddit_social_ms

WORKDIR /Twiddit_social_ms

COPY . .

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ARG URL=0.0.0.0:4000

CMD [ "sh", "-c", "python manage.py makemigrations relationship && python manage.py migrate && python manage.py runserver $URL" ]
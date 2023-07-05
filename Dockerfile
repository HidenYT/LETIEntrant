FROM python:3.9

WORKDIR usr/src/app

ENV DJANGO_LETIENTRANT_SECTET_KEY=django-insecure-xkfcam$l^kxz0%v#l-5xvdxy&-a2t3vx^mwkg!%ut(pe&r9a9j

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
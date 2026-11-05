#FROM python:3.13

#ENV PYTHONUNBUFFERED=1

#RUN mkdir /app

#COPY requirements.txt /app/

#COPY mysite /app/

#RUN pip install -r /app/requirements.txt

#WORKDIR /app

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "runserver"]

# docker build -t app .
# docker run -p 8000:8000 app


##########################################################################
# docker-compose
#####################################################################

# с docker-compose
# docker compose version
# docker compose build app
# docker compose up app


FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY mysite .

# Обязательно собираем статику перед запуском
RUN python manage.py collectstatic --noinput

# Запускаем через промышленный сервер Gunicorn (вместо mysite.wsgi укажите имя вашей папки с settings.py)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]




# RUN python manage.py collectstatic
#COPY mysite .
#CMD ["python", "manage.py", "runserver","0.0.0.0:8080"]
#CMD ["python", "manage.py", "runserver"]
#CMD ["gunicorn","mysite.wsgi:application","--bind","0.0.0.0:8080"]


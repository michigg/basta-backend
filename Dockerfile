FROM alpine:3.6
RUN apk upgrade --update
RUN apk add --update python3
RUN apk add --update py3-pillow
RUN pip3 install django==1.11.7 django-jinja django-rest-framework django-analytical
ADD ["ofu_app", "/app"]
WORKDIR /app
EXPOSE 8080
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
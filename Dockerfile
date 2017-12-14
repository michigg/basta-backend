FROM alpine:3.6
RUN apk upgrade --update && \
	apk add --update python3 py3-pillow py3-lxml && \
	pip3 install django==1.11.7 django-jinja django-rest-framework django-analytical requests beautifulsoup4
ADD ["ofu_app", "/app"]
WORKDIR /app
EXPOSE 80
VOLUME ["/app/db.sqlite"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]

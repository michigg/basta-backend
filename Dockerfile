FROM alpine:3.6
ADD ["ofu_app/requirements.txt", "/requirements.txt"]
RUN apk upgrade --update && \
	apk add --update python3 py3-pillow py3-lxml py3-psycopg2 && \
	pip3 install -r /requirements.txt && rm /requirements.txt
WORKDIR /app
EXPOSE 80
VOLUME ["/app/data"]
VOLUME ["/app/media"]
ENTRYPOINT ["python3", "manage.py"]
ADD ["ofu_app", "/app"]
CMD ["runserver", "0.0.0.0:80"]

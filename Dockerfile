FROM python:3.6.9-alpine


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP /usr/src/app/transfer_flask/run.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 5000

RUN ls -la transfer_flask/

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

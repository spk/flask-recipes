FROM python:3.8-alpine

ENV APP_USER recipes
ENV APP_ROOT /code
ENV PYTHONUNBUFFERED 1

RUN addgroup -g 1000 ${APP_USER} && \
    adduser -u 1000 -h ${APP_ROOT} -D -G ${APP_USER} ${APP_USER}

RUN apk add --no-cache \
        gcc \
        python3-dev \
        musl-dev \
        postgresql-dev

WORKDIR ${APP_ROOT}
ADD requirements.txt ${APP_ROOT}/
RUN pip install -r requirements.txt
USER ${APP_USER}
ADD . ${APP_ROOT}

FROM python:2.7

ENV APP_USER recipes
ENV APP_ROOT /code
ENV PYTHONUNBUFFERED 1
# ENV PYTHONPATH=/code/flask-bootstrap/

RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_ROOT}
ADD requirements.txt ${APP_ROOT}/
RUN pip install -r requirements.txt
USER ${APP_USER}
ADD . ${APP_ROOT}

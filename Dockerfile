FROM python:3.10-buster

ENV APP_DIR=/api
ENV SOURCE_ROOT=$APP_DIR/src/

RUN mkdir -p ${APP_DIR}
WORKDIR $APP_DIR

COPY Pipfile Pipfile.lock $APP_DIR

RUN python -m pip install pipenv
RUN python -m pipenv install

COPY . $APP_DIR
ENV PYTHONPATH "${PYTHONPATH}:$SOURCE_ROOT"
WORKDIR $SOURCE_ROOT

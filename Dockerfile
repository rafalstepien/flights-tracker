FROM python:3.9.10-alpine as python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.12 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths: this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apk update \
    && apk add --no-cache gcc libffi-dev musl-dev postgresql-dev build-base

RUN pip install "poetry==$POETRY_VERSION"

COPY ./flights-tracker /home/flights-tracker
COPY ./poetry.lock /home/flights-tracker/
COPY ./pyproject.toml /home/flights-tracker/
ENV ENV_FILE="/home/flights-tracker/config/local.env"

WORKDIR /home/flights-tracker/

RUN poetry config virtualenvs.create false

RUN poetry install

CMD ["python", "/home/flights-tracker/flights_tracker/tracker.py"]
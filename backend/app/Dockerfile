FROM python:3.9

LABEL maintainer="Ícaro Ribeiro <icaroribeiro@hotmail.com>"

WORKDIR /app

COPY . .

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH="$PYTHONPATH:/app"

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 \
    && chmod 755 ${POETRY_HOME}/bin/poetry

RUN poetry install --only main --no-root --no-ansi

CMD [ "sh", "-c", "python src/main.py" ]

# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# It starts from the python base image.
FROM python:3.10

# Add maintainer info.
LABEL maintainer="Ícaro Ribeiro <icaroribeiro@hotmail.com>"

# Set the working directory inside the container.
WORKDIR /app

# Copy the source from the current directory to the working directory inside the container.
COPY . .

# Set up environment variables.
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# It is to run poetry directly as soon as it's installed.
ENV PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH="$PYTHONPATH:/app"

# Install curl and poetry.
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 \
    && chmod 755 ${POETRY_HOME}/bin/poetry

# Create the folder /app/.venv and install runtime dependencies.
RUN poetry install --only main --no-root --no-ansi

# Command to run the application.
CMD [ "sh", "-c", "poetry run python comd/api/main.py" ]

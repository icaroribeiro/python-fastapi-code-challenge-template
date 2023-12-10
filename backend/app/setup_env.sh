#!/bin/bash

export PYTHONPATH="$PWD"

export HTTP_PORT="5000"

export DB_DRIVER="postgresql+asyncpg"
export DB_USER="root"
export DB_PASSWORD="root"
export DB_HOST="localhost"
export DB_PORT="5433"
export DB_NAME="db"

export MAX_CONTENT_SIZE="1048576"
export UPLOAD_FOLDER="./../uploads"
export ALLOWED_EXTENSIONS="txt"
export MAX_LINE_LENGTH="86"

export MINIMUM_PAGE_NUMBER="1"
export MINIMUM_PAGE_SIZE="5"
export MAXIMUM_PAGE_SIZE="20"

export PRIVATE_KEY_FILE_PATH="./config/jwtRS256.key"
export PUBLIC_KEY_FILE_PATH="./config/jwtRS256.key.pub"
export ACCESS_TOKEN_EXPIRES_IN=60
export REFRESH_TOKEN_EXPIRES_IN=1440
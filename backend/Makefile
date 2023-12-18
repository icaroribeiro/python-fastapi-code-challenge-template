#
# Backend application
# Set of tasks related to the local building of backend application.
#
lint-app:
	cd ./app; \
	poetry run black --check --diff .; \
	poetry run isort --check --diff .


format-app:
	cd ./app; \
	poetry run black .; \
	poetry run isort .


setup-db:
	cd ./db; \
	find . -iname "*.sql" | xargs printf -- ' -f %s' | xargs -t psql -p 5433 -U postgres -d db


start-dependencies:
	cd ./db; \
	docker build -t db-image --no-cache -f Dockerfile .; \
	docker run --name db-container --env-file .env -d -p 5433:5432 -v db-container-data:/var/lib/postgresql/data --restart on-failure db-image


finish-dependencies:
	docker stop db-container; \
	docker rm db-container; \
	docker volume rm db-container-data; \
	docker rmi db-image


run-app:
	cd ./app; \
	. ./setup_env.sh; \
	poetry run python src/main.py


test-app:
	cd ./app; \
	. ./setup_env.sh; \
	poetry run pytest --no-cov-on-fail --cov-fail-under=50 -v test


check-app-coverage:
	cd ./app; \
	. ./setup_env.sh; \
	poetry run pytest --cov=src --no-cov-on-fail -v test


#
# Dockerized Backend application
# Set of tasks related to the testing of dockerized backend application.
#
start-dockerized-app-dependencies:
	cd ./db; \
	docker network create app-db-network; \
	docker build -t db-image --no-cache -f Dockerfile .; \
	docker run --name db-container --env-file .env -d -p 5433:5432 -v db-container-data:/var/lib/postgresql/data --restart on-failure db-image
	docker network connect app-db-network db-container


run-dockerized-app:
	cd ./app; \
	docker build -t app-image -f Dockerfile .; \
	docker run --name app-container --env-file .env -d -p 5000:5000 --restart on-failure app-image; \
	docker network connect app-db-network app-container


destroy-dockerized-app:
	docker network disconnect app-db-network app-container; \
	docker stop app-container; \
	docker rm app-container; \
	docker rmi app-image


finish-dockerized-app-dependencies:
	docker network disconnect app-db-network db-container; \
	docker stop db-container; \
	docker rm db-container; \
	docker volume rm db-container-data; \
	docker rmi db-image; \
	docker network rm app-db-network


test-dockerized-app:
	cd ./app; \
	docker exec --env-file .env app-container poetry run pytest --no-cov-on-fail --cov-fail-under=50 -v test


check-dockerized-app-coverage:
	cd ./app; \
	docker exec --env-file .env app-container poetry run pytest --cov=src --no-cov-on-fail -v test

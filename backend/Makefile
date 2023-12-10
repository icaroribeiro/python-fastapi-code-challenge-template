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

run-app:
	cd ./app; \
	. ./setup_env.sh; \
	poetry run python src/main.py


unittest-app:
	cd ./app; \
	. ./setup_env.sh; \
    poetry run pytest --no-cov-on-fail --cov-fail-under=50 -v tests


unittest-coverage-app:
	cd ./app; \
	. ./setup_env.sh; \
	poetry run pytest --cov=src --no-cov-on-fail -v tests


#
# Dockerized Backend application
# Set of tasks related to the testing of dockerized backend application.
#
start-app-dependencies:
	cd ./db; \
	docker network create testapp_network; \
	docker build -t postgresdb --no-cache -f Dockerfile .; \
	docker run --name postgresdb_container --env-file .env -d -p 5433:5432 -v postgresdb-data:/var/lib/postgresql/data --restart on-failure postgresdb
	docker network connect testapp_network postgresdb_container


finish-app-dependencies:
	docker network disconnect testapp_network postgresdb_container; \
	docker stop postgresdb_container; \
	docker rm postgresdb_container; \
	docker volume rm postgresdb-data; \
	docker rmi postgresdb; \
	docker network rm testapp_network


init-dockerized-app:
	cd ./app; \
	docker build -t backend -f Dockerfile .; \
	docker run --name backend_container --env-file .env -d -p 5000:5000 --restart on-failure backend; \
	docker network connect testapp_network backend_container


destroy-dockerized-app:
	docker network disconnect testapp_network backend_container; \
	docker stop backend_container; \
	docker rm backend_container; \
	docker rmi backend


unittest-dockerized-app:
	cd ./app; \
	docker exec --env-file .env backend_container poetry run pytest --no-cov-on-fail --cov-fail-under=50 -v tests


unittest-coverage-dockerized-app:
	cd ./app; \
	docker exec --env-file .env backend_container poetry run pytest --cov=src --no-cov-on-fail -v tests

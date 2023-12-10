startup:
	docker-compose up -d --build

shutdown:
	docker-compose down -v --rmi all
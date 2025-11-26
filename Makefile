.PHONY: test lint run build backup list stop restart ready

ready: lint test


test:
	cd backend && PYTHONPATH=. pytest

lint:
	cd backend && ruff check . && mypy --explicit-package-bases .

run:
	docker-compose up --build

build:
	docker-compose build

backup:
	./scripts/backup.sh

list:
	./scripts/list_servers.sh

stop:
	./scripts/stop_server.sh

restart: stop run

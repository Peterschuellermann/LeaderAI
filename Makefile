.PHONY: test lint run build backup

test:
	cd backend && pytest

lint:
	cd backend && ruff check . && mypy .

run:
	docker-compose up --build

build:
	docker-compose build

backup:
	./scripts/backup.sh


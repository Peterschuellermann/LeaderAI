.PHONY: test lint run build backup

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

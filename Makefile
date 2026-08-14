.PHONY: up down build ps logs shell restart

up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

ps:
	docker compose ps

logs:
	docker compose logs -f gateway

restart:
	docker compose down
	docker compose up --build
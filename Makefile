.PHONY: run,up

ENV_FILE ?= .env.local
COMPOSE = docker-compose -f deploy/local/docker-compose.yaml --env-file "$(ENV_FILE)"

include ${ENV_FILE}

run:
	uv run python3 main.py $(ARGS)

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

migrate:
	goose -dir migrations postgres \
	"postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)\
	@$(POSTGRES_OUTER_HOST):$(POSTGRES_PORT)/$(POSTGRES_NAME)\
	?sslmode=$(SSL_MODE)" up


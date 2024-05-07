.PHONY: test
test:
	@poetry run pytest

.PHONY: run
run:
	@poetry run uvicorn KsdNaverOCRServer.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: deploy
deploy:
	nohup make run


.PHONY: lint
lint:
	@poetry run ruff check . --fix



.PHONY: format
format:
	@poetry run ruff format .


local-compose-up
	@docker compose -f ./docker-compose.yml up -d

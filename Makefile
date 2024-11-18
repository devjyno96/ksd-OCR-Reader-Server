.PHONY: test
test:
	@poetry run pytest

.PHONY: run
run:
	@poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: deploy
deploy:
	nohup make run

.PHONY: admin-run
admin-run:
	@poetry run streamlit run ./app/streamlit_admin.py

.PHONY: lint
lint:
	@poetry run ruff check . --fix



.PHONY: format
format:
	@poetry run ruff format .


.PHONY: shell
shell:
	@poetry run ipython


.PHONY: PHONY
local-compose-up:
	@docker compose -f ./docker-compose.yml up -d

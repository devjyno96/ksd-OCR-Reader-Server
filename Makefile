.PHONY: init
init:
	pip3 install --upgrade pip
	python3 -m pip install --upgrade setuptools
	pip3 install -r requirements.txt

.PHONY: test
test: 
	pytest

.PHONY: run 
run: 
	uvicorn KsdNaverOCRServer.main:app --workers 2 --host 0.0.0.0 --port 8000

.PHONY: deploy
deploy: 
	supervisord -c ./deploy/supervisord.conf
.PHONY: init  ## Install the package, dependencies, and pre-commit for local development
init:
	pip3 install --upgrade pip
	python3 -m pip install --upgrade setuptools
	pip3 install -r requirements.txt

.PHONY: test  ## Run all tests, skipping the type-checker integration tests
test: 
	pytest

.PHONY: test build upload
.DEFAULT_GOAL := help

help: ## Shows this help menu
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test: ## execute all tests
	python -m unittest discover -s tests

build: ## build the project into whl
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*
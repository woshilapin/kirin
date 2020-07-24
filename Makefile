setup_for_test: ## Setup basic environment for tests
	apt update && apt install -y protobuf-compiler virtualenv
	rm -rf venv && virtualenv venv && . venv/bin/activate
	rm -rf .pytest_cache
	find . -name *.pyc -name __pycache__ -exec rm -rfv {} \;

test: ## Launch all tests
	pip install -r requirements_dev.txt -U
	python setup.py build_version
	python setup.py build_pbf
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. KIRIN_CONFIG_FILE=test_settings.py \
		py.test -v --doctest-modules -p no:cacheprovider \
		--cov-report xml --junitxml=pytest_kirin.xml --cov=kirin .

help: ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' $(CURDIR)/$(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup_for_test test help
.DEFAULT_GOAL := help

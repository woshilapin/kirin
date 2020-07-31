KISIO_TEMP_DOCKER_REGISTRY := tmp-docker-registry.canaltp.fr
KIRIN_CI_DOCKER_NAMESPACE := ${KISIO_TEMP_DOCKER_REGISTRY}/kirin
KIRIN_CI_INTEGRATION_IMAGE := kirin_test_context

build_test_context: ## Build context image for tests
	$(info Building context image for tests)
	-@docker pull ${KIRIN_CI_DOCKER_NAMESPACE}/${KIRIN_CI_INTEGRATION_IMAGE}:latest
	@docker build -t ${KIRIN_CI_DOCKER_NAMESPACE}/${KIRIN_CI_INTEGRATION_IMAGE}:latest tests

push_test_context: build_test_context ## Push context image for tests
	$(info Pushing context image for tests)
	@docker push ${KIRIN_CI_DOCKER_NAMESPACE}/${KIRIN_CI_INTEGRATION_IMAGE}:latest

test_in_context: push_test_context ## Launch all tests in context image
	$(info Launching tests in context image)
	docker run --rm \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume "${PWD}":/tmp/workspace \
		--workdir /tmp/workspace \
		${KIRIN_CI_DOCKER_NAMESPACE}/${KIRIN_CI_INTEGRATION_IMAGE}:latest \
		sh -c "make test"

test: ## Launch all tests
	./tests/launch_tests.sh

help: ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' $(CURDIR)/$(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test help build_test_context push_test_context test_in_context
.DEFAULT_GOAL := help

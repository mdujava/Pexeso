.PHONY: commit-acceptance pylint flake8 mypy black-check \
	pipenv pipenv-dev \
	clean

SHELL = /bin/bash

PIPENV_VERBOSITY ?= -1
PIPENV_IGNORE_VIRTUALENVS ?= 1

ifdef PYTHON_VERSION
PIPENV_ARGS += --python $(PYTHON_VERSION)
endif

commit-acceptance: pylint flake8 mypy black-check

pylint flake8 mypy: pipenv-dev
	pipenv run $@ $(flags) .

black-check: pipenv-dev
	pipenv run black --check .

Pipfile.lock: Pipfile
	pipenv lock $(PIPENV_ARGS)

.make-pipenv-sync: Pipfile.lock
	pipenv sync $(PIPENV_ARGS)
	touch .make-pipenv-sync

.make-pipenv-sync-dev: Pipfile.lock
	pipenv sync --dev $(PIPENV_ARGS)
	touch .make-pipenv-sync-dev .make-pipenv-sync

pipenv: .make-pipenv-sync

pipenv-dev: .make-pipenv-sync-dev

clean: ## clean pip deps
clean: mostlyclean
	rm -f Pipfile.lock

mostlyclean:
	rm -f .make-*
	rm -rf .mypy_cache
	-pipenv --rm

# Check http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

fake-sync:
	test -e Pipfile.lock \
		&& touch Pipfile.lock \
		&& touch .make-pipenv-sync .make-pipenv-sync-dev \
		|| true

# this ensures dependent target is run everytime
FORCE:

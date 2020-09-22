
define check_env_variable
$(if $(strip $($1)),,$(error "$1" ENV VARIABLE IS REQUIRED!))
endef

ifndef EDITOR
	ifneq ("$(wildcard /etc/alternatives/editor)","")
		EDITOR := /etc/alternatives/editor
	else
		EDITOR := vi
	endif
endif

venv: requirements-dev.txt setup.py setup.cfg
	deactivate || true
	rm -rf venv/  # Ensure that venv does not exist
	tox -e venv
	venv/bin/pre-commit install --install-hooks

.PHONY: development
development: venv
	@true

.PHONY: test
test:
	tox ${TOX_ARGS}

.PHONY: clean
clean:
	rm -rf .tox/ .pytest_cache/ .coverage venv/
	find -name *.pyc -delete

.PHONY: release
release:
	$(eval $(call check_env_variable,NEXT_VERSION))
ifneq ($(shell git rev-parse --abbrev-ref HEAD),master)
	$(error `make release` could be execute only on master branch)
endif
	echo "Running tests for extra safety"
	sed -ri "s/^(version = ).*/\1${NEXT_VERSION}/" setup.cfg
	sed -ri "s/^(=+)$$/\1\n\n${NEXT_VERSION} ($$(date "+%Y-%m-%d"))\n------------------\n- TODO: add notes/" CHANGELOG.md
	${EDITOR} CHANGELOG.md
	git add --patch setup.cfg CHANGELOG.md
	git commit -m "Release version ${NEXT_VERSION}"
	git tag "v${NEXT_VERSION}"
	git push origin --atomic master "v${NEXT_VERSION}"


define check_env_variable
$(if $(strip $($1)),,$(error "$1" ENV VARIABLE IS REQUIRED!))
endef


venv: requirements-dev.txt setup.py language_formatters_pre_commit_hooks/__init__.py
	rm -rf venv/  # Ensure that venv does not exist
	tox -e venv
	venv/bin/pre-commit install --install-hooks

.PHONY: development
development: venv
	@true

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	rm -rf .tox/ .pytest_cache/ .coverage venv/
	find -name *.pyc -delete
	find -name __pycache__ -type d -exec rm -rf ${CURDIR}/{} \;

.PHONY: release
release: venv
	$(eval $(call check_env_variable,NEXT_VERSION))
ifneq ($(shell git rev-parse --abbrev-ref HEAD),master)
	$(error `make release` could be execute only on master branch)
endif
	sed -ri "s/(__version__ = )'.*'/\1'${NEXT_VERSION}'/" language_formatters_pre_commit_hooks/__init__.py
	# TODO: add commands to modify CHANGELOG.rst while running makefile target
	git add --patch language_formatters_pre_commit_hooks/__init__.py CHANGELOG.rst
	git commit -m "Release version ${NEXT_VERSION}"
	git tag "v${NEXT_VERSION}"
	echo "Running tests for extra safety"
	$(MAKE) test
	echo "Clean old artifacts"
	rm -rf build/ dist/
	venv/bin/python setup.py sdist bdist_wheel
	# TODO: build wheels for more platforms if needed
	venv/bin/twine upload -r pypi dist/*
	git push origin master --tags

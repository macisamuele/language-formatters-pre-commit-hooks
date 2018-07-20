
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

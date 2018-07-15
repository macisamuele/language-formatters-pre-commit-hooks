
venv:
	virtualenv venv
	venv/bin/pip install -r requirements-dev.txt
	venv/bin/pre-commit install --install-hooks

.PHONY: development
development: venv
	@true

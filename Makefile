.PHONY: all run egg test coverage clean

all: run

run:
	@python app

dep:
	@pip install -r requirements.txt

egg:
	@python setup.py sdist bdist_wheel

egg-check: egg
	@twine check dist/*

test:
	@pytest tests

coverage:
	@pytest --cov=app tests/

pypi-test: egg egg-check
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-prod: egg egg-check
	@twine upload dist/*

clean:
	@find . -type f -name ".mypy_cache" -print0 | xargs -r0 -- rm -r
	@find . -type d -name ".pytest_cache" -print0 | xargs -r0 -- rm -r
	@find . -type d -name "__pycache__" -print0 | xargs -r0 -- rm -r
	@find . -type d -name "*.pyc" -print0 | xargs -r0 -- rm -r
	@rm -rf *.egg-info build dist .coverage

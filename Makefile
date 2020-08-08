ENV=pipenv

.PHONY: init run test egg clean

all: run

init:
	@$(ENV) sync
	@$(ENV) run pre-commit install

run:
	@python minesweeper

test:
	@$(ENV) run pytest --cov=minesweeper tests

egg:
	@$(ENV) run python setup.py sdist bdist_wheel

clean:
	@find . -type f -name ".mypy_cache" -print0 | xargs -r0 -- rm -r
	@find . -type d -name ".pytest_cache" -print0 | xargs -r0 -- rm -r
	@find . -type d -name "__pycache__" -print0 | xargs -r0 -- rm -r
	@find . -type d -name "*.pyc" -print0 | xargs -r0 -- rm -r
	@rm -rf *.egg-info build dist .coverage

ENV=pipenv
SRC=minesweeper
.PHONY: init run-basic run-intermediate run-expert test egg clean

init:
	@$(ENV) sync
	@$(ENV) run pre-commit install

run-basic:
	@$(ENV) run python $(SRC) basic

run-intermediate:
	@$(ENV) run python $(SRC) intermediate

run-expert:
	@$(ENV) run python $(SRC) expert

test:
	@$(ENV) run pytest --cov=$(SRC) tests

egg: clean
	@$(ENV) run python setup.py sdist bdist_wheel

clean:
	@find . -type f -name ".mypy_cache" -print0 | xargs -r0 -- rm -r
	@find . -type d -name ".pytest_cache" -print0 | xargs -r0 -- rm -r
	@find . -type d -name "__pycache__" -print0 | xargs -r0 -- rm -r
	@find . -type d -name "*.pyc" -print0 | xargs -r0 -- rm -r
	@rm -rf *.egg-info build dist .coverage

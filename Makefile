format:
	yapf -i -r --style=google src

run:
	pipenv run python src/main.py
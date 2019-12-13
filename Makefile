all:
	make lint
	make test

lint:
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --ignore=C901

test:
	python3 test.py

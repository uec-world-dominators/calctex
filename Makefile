all:
	make lint
	make test

lint:
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --ignore=C901

test:
	python3 test.py

pypi:
	python3 setup.py bdist_wheel
	twine upload --repository pypi dist/*

clean:
	rm -rf dist build *.egg-info
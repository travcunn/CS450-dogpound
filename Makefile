clean:
	find . -name *.pyc -delete

run:
	python run.py

test: coverage-run coverage-report

coverage-run:
	coverage run tests.py

coverage-report:
	coverage report

install:
	pip install -r requirements.txt

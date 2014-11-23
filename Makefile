clean:
	find . -name *.pyc -delete

db-create:
	python db_create.py

run:
	python run.py

jenkins-test:
	nosetests --with-coverage --with-xunit --cover-package=app --cover-erase

test: coverage-run coverage-report

coverage-run:
	coverage run tests.py

coverage-report:
	coverage report

install:
	pip install -r requirements.txt

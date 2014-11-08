clean:
	find . -name *.pyc -delete

run:
	python run.py

test:
	python tests.py

install:
	pip install -r requirements.txt

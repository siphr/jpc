.PHONY: requirements requirements_test clean lint test run build

TEST_PATH=./tests
REV=`git rev-parse --short HEAD 2> /dev/null | sed "s/\(.*\)/@\1/"`

requirements:
	pip install -r requirements.pip

clean:
	find . -type f -name '*.py[co]' -delete && \
	rm -rf build

lint:
	flake8 --exclude=env,venv

test: clean
ifndef TEST_ONLY
	TEST_ONLY=$(TEST_PATH)
endif
	python -m pytest --color=yes --cov-report term --cov=. $(TEST_ONLY) && \
	$(MAKE) stop_test_db_server 2> /dev/null; true  # Try and kill the container, but don't panic if we're not using one

run:
	python main.py

build: clean
	mkdir -p build
	zip -r build/property_service_$(REV).zip . -x deploy/\* build/\* env/\* venv/\* __pycache__/\* */\.* */\.pyc \.git/\* \.cache/\*

.PHONY: requirements clean lint test run build

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
	python -m pytest --color=yes --cov-report term --cov=. $(TEST_ONLY)

run:
	python main.py

build: clean
	mkdir -p build
	zip -r build/super_simple_stock_market_$(REV).zip . -x .coverage .*.un~ build/\* env/\* venv/\* .pytest_cache/\* */__pycache__/\* */\.* */\.pyc \.git/\* \.cache/\*

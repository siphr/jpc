.PHONY: requirements clean lint test build

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
	python -m pytest --color=yes --cov-report term --cov=super_simple_stock_market $(TEST_ONLY)

coverage: clean
	python -m pytest --color=yes --cov-report xml --cov=super_simple_stock_market $(TEST_ONLY)

build: clean
	mkdir -p build
	zip -r build/super_simple_stock_market_$(REV).zip . -x .coverage .*.un~ build/\* env/\* venv/\* .pytest_cache/\* */__pycache__/\* */\.* */\.pyc \.git/\* \.cache/\*

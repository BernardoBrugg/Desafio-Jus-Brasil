PYTHON = .venv/bin/python
ENV_VARS = PYTHONPATH=.

.PHONY: help install test run benchmark submission clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install     Install project dependencies"
	@echo "  make test        Execute all unit and integration tests"
	@echo "  make run         Process documents and generate output JSONs"
	@echo "  make benchmark   Run evaluation against the golden set"
	@echo "  make submission  Generate submission.csv and submission.zip"
	@echo "  make clean       Remove temporary files, cache, and outputs"

install:
	pip install -r requirements.txt

test:
	$(ENV_VARS) $(PYTHON) -m unittest discover tests

run:
	$(ENV_VARS) $(PYTHON) src/cli/run_pipeline.py

benchmark:
	$(ENV_VARS) $(PYTHON) src/cli/run_evaluation.py

submission: run
	$(ENV_VARS) $(PYTHON) scripts/json_to_submission.py --input-dir ./output --output-file ./submission.csv
	$(ENV_VARS) $(PYTHON) scripts/package_submission.py --input-dir ./output --zip-file ./submission.zip

clean:
	rm -rf output submission.csv submission.zip matches .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t caca-alucinacoes-bracis .

docker-run:
	docker run --rm -v $(PWD)/data/in:/data/in -v $(PWD)/data/out:/data/out caca-alucinacoes-bracis --input /data/in --output /data/out

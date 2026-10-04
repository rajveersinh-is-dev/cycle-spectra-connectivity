# Convenience targets.  Nothing here is required; see README.md.

PY ?= python
MAXN ?= 9

.PHONY: help install test validate experiments smoke figures paper all clean

help:
	@echo "make install    install dependencies"
	@echo "make test       run the test suite (~3 min)"
	@echo "make validate   brute-force validation of the generators, n <= 6"
	@echo "make experiments  full pipeline, orders up to $(MAXN) (~12 min)"
	@echo "make smoke      pipeline smoke run, orders up to 6 (<1 min)"
	@echo "make paper      compile paper/main.tex (needs a LaTeX distribution)"
	@echo "make all        test + experiments"

install:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest tests -q

validate:
	$(PY) scripts/validate_generators.py 6

experiments:
	$(PY) experiments/run_all.py --max-n $(MAXN)

smoke:
	$(PY) experiments/run_all.py --max-n 6

figures:
	$(PY) experiments/stage6_figures.py

paper:
	cd paper && pdflatex -interaction=nonstopmode main.tex

all: test experiments

clean:
	rm -rf results figures .pytest_cache **/__pycache__
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
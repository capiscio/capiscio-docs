.PHONY: install serve build clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
MKDOCS = $(VENV)/bin/mkdocs

$(VENV)/bin/activate: requirements-docs.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements-docs.txt
	touch $(VENV)/bin/activate

install: $(VENV)/bin/activate

serve: install
	$(MKDOCS) serve

build: install
	$(MKDOCS) build

clean:
	rm -rf $(VENV)
	rm -rf site

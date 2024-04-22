##### VARIABLES
ENV = venv
VENV = $(ENV)/bin/activate
PIP = $(ENV)/bin/pip
PYTHON = $(ENV)/bin/python
TWINE = $(ENV)/bin/twine
PORT = 8000
VERSION = 4.2

$(VENV):
	##### create virtualenv
	test -d $(VENV) || virtualenv $(ENV) --prompt="(django-frontify)"
	$(PIP) install --upgrade pip

build:
	docker build -t django-frontify:base -f Dockerfile .

django_frontify.egg-info: $(VENV)
	$(PIP) install -e .
	$(PIP) install -r tests/requirements/django-$(VERSION).txt

clean:
	rm -rf *testdb.sqlite
	rm -rf node_modules
	rm -rf venv
	rm -rf django_frontify.egg-info
	rm -rf dist

node_modules:
	npm install

test_release: django_frontify.egg-info node_modules
	npm run build
	$(PYTHON) setup.py bdist_wheel
	$(TWINE) upload -r pypitest dist/*

release: django_frontify.egg-info node_modules
	npm run build
	$(PYTHON) setup.py bdist_wheel
	$(TWINE) upload dist/*

watch_static: node_modules
	npm run watch

runserver: django_frontify.egg-info
	$(PYTHON) example/manage.py runserver

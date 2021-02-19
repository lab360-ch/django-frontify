PORT = 8000
VERSION = 2.2

build:
	docker build -t django-frontify:base -f Dockerfile .

cleanup:
	rm -rf *testdb.sqlite
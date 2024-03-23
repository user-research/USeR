UID := $(shell id -u)
GID := $(shell id -g)

docker-compose := env UID=${UID} GID=${GID} docker compose
names := title persona what why acceptance_criteria additionals attachments
projects := p1

build:
	${docker-compose} build

up:
	${docker-compose} up

ready: clean import train predict percentiles test

stop:
	${docker-compose} stop

restart:
	${docker-compose} restart

clean:
	rm -rf ./api/cache/*

train:
	@for project in ${projects} ; do \
		echo "make train: $$project" ; \
		${docker-compose} exec api pipenv run python manage.py train $$project ; \
	done

import:
	@for project in ${projects} ; do \
	echo "make import: $$project" ; \
		${docker-compose} exec api pipenv run python manage.py import $$project ; \
	done

predict:
	rm -f ./api/cache/predictions*.csv
	${docker-compose} exec api pipenv run python manage.py generate_predictions

percentiles:
	rm -f ./api/cache/percentiles*.csv
	${docker-compose} exec api pipenv run python manage.py generate_percentiles

test:
	rm -rf ./api/tests/cache/*
	${docker-compose} exec api pipenv run python -m unittest discover -v tests

debug:
	${docker-compose} exec api pipenv run python manage.py debug
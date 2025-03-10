UID := $(shell id -u)
GID := $(shell id -g)

docker-compose := env UID=${UID} GID=${GID} docker compose

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
	${docker-compose} exec api pipenv run python manage.py train

import:
	${docker-compose} exec api pipenv run python manage.py import

predict:
	${docker-compose} exec api pipenv run python manage.py generate_predictions

percentiles:
	${docker-compose} exec api pipenv run python manage.py generate_percentiles

test:
	${docker-compose} exec api pipenv run python -m unittest discover -v tests
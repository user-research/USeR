FROM python:3.10-slim-bullseye AS base
# https://stackoverflow.com/questions/71591971/how-can-i-fix-the-zsh-command-not-found-python-error-macos-monterey-12-3
# pyenv local python installation

RUN apt-get update && \ 
    apt-get upgrade && \
    apt-get install -y perl gcc
RUN apt-get clean all

WORKDIR /usr/src/user

RUN pip install --upgrade pip setuptools wheel && \
    pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --verbose && \
    pipenv run python -m spacy download de_core_news_lg

COPY . .

ENTRYPOINT ["pipenv", "run", "python" , "-m" , "flask"]
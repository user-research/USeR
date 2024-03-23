FROM python:3.10-slim-bullseye as base
# https://stackoverflow.com/questions/71591971/how-can-i-fix-the-zsh-command-not-found-python-error-macos-monterey-12-3
# pyenv local python installation

RUN apt-get update && \ 
    apt-get upgrade && \
    apt-get install -y perl gcc
RUN apt-get clean all

WORKDIR /usr/src/user

RUN pip install --upgrade pip && \
    pip install pipenv

COPY Pipfile .
#TODO: Fix problem with torch and Mac x86/arm architecture
#Current lockfile works with Mac silicon/arm
#COPY Pipfile.lock .

RUN pipenv install --verbose && \
    pipenv run python -m spacy download de_core_news_md

COPY . .

ENTRYPOINT ["pipenv", "run", "python" , "-m" , "flask"]
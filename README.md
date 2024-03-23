This is the code repository of USeR a User Story Evaluation Robot.

USeR is a web-based user story eReviewer tool that allows authors like product owners in agile software projects to assess and optimize user story quality through a user interface for instant, consistent, and explainable user feedback supporting fast and easy quality optimizations.

This repository implements USeR and a small user stories example dataset.


# Create a new environment
```
make build
```

# Start app
```
make up
http://localhost:3000
```

# Starting with an empty app, change config options in /config/user/default.cfg
 
# 1. Define first your project identifier(s). Multiple projects are possible, separated by a comma (,p2,p3)
 
[app]
projects = p1

# 2. Add the common word list, which will be used in the `Easy Language` metric
 
[lists.de]
basic_words = ./data/basic.words.de.csv
 
# 3. Configure the spaCy model, which handles e.g., tokenizations and text embeddings
 
[ai]
https://spacy.io/usage/models
spacy_model = de_core_news_lg

# 4. Provide the backlog path and filename to the project user stories.
# The variable {project} should match the previously defined project name `projectA`

[project]
corpus_raw_file = ./importer/corpus.{project}.raw.csv
corpus_file = ./data/corpus.{project}.csv
#
# 5. Create a project importer in the importer folder e.g. P1Importer.py that imports the raw user stories into the /data folder. 
# The importer can be adapted to the project-specific CSV format.
```
make ready
```

# Restart app
```
make restart
```

# Tests
## Run all tests
```
make test
```

# Shutdown environment
```
make stop
```

# Init config and train spacy pipeline [SpaCy training](https://spacy.io/usage/training)
## If your config contains missing values, you can run the 'init fill-config'
```
docker compose exec api pipenv run python -m spacy init fill-config ./config/spacy/base_config.cfg ./config/spacy/[p1|p2].de.cfg
docker compose exec api pipenv run python -m spacy init fill-config ./config/spacy/[p1|p2].de.cfg ./config/spacy/[p1|p2].de.cfg
```

# Generate Spacy test and dev data
## You can now add your data and train your pipeline:
```
docker compose exec api pipenv run python -m spacy train ./config/spacy/[p1|p2].de.cfg --output ./output/[p1|p2]
```

# Debug config and data [SpaCy debug-data](https://spacy.io/api/cli#debug-data)
```
docker compose exec api pipenv run python -m spacy debug config ./config/spacy/[p1|p2].de.cfg
docker compose exec api pipenv run python -m spacy debug data ./config/spacy/[p1|p2].de.cfg --verbose
```

# Get installed versions 5. Oct, 2023
```
docker --version
```
- 24.0.6


```
docker compose exec api uname -r
```
- 5.15.49-linuxkit


```
docker compose exec api pipenv run python --version
```
- Python 3.10.13

```
docker compose exec api pipenv run python -m flask --version
```
- Python 3.10.13
- Flask 2.3.3
- Werkzeug 2.3.7


```
docker compose exec api pipenv run python -m spacy info
```
- spaCy version 3.6.1                         
- Location /root/.local/share/virtualenvs/user-9iY0gKSr/lib/python3.10/site-packages/spacy
- Platform Linux-6.4.16-linuxkit-aarch64-with-glibc2.31
- Python version 3.10.13                       
- Pipelines de_core_news_sm (3.6.0) 

```
docker compose exec api pipenv run pip show scikit-learn
```
- Name: scikit-learn
- Version: 1.2.0

```
docker compose exec api pipenv run pip show bertopic
```
- Name: bertopic
- Version: 0.15.0


```
docker compose exec web node --version
```
- v20.6.1

```
docker compose exec web npm view react version
```
- 18.2.0

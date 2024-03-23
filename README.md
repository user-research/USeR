# USeR
This is the code repository of USeR a User Story Evaluation Robot.

USeR is a web-based user story eReviewer tool that allows authors like product owners in agile software projects to assess and optimize user story quality through a user interface for instant, consistent, and explainable user feedback supporting fast and easy quality optimizations.

This repository implements USeR and a small "demo" user stories dataset.

## Create a new environment
```
make build
```

## Start app
```
make up
http://localhost:3000
```

Starting with an empty app, change config options in /config/user/default.cfg

1. Define first your project identifier(s). Multiple projects are possible, separated by a comma (,p2,p3)

```
[app]
projects = p1
```

2. Add the common word list, which will be used in the `Easy Language` metric

``` 
[lists.de]
basic_words = ./data/basic.words.de.csv
```

3. Configure the spaCy model, which handles e.g., tokenizations and text embeddings

```
[ai]
https://spacy.io/usage/models
spacy_model = de_core_news_lg
```

4. Provide the backlog path and filename to the project user stories.
The variable {project} should match the previously defined project name **p1**

```
[project]
backlog_raw_file = ./importer/backlog.{project}.raw.csv
backlog_file = ./data/backlog.{project}.csv
```

5. Update the P1Importer.py (or create a new *Importer.py) that imports the raw user stories into the /data folder. 
The importer can be adapted to the project-specific CSV format.

6. Finally, execute:

```
make ready
```

## Restart app
```
make restart
```

## Tests

Run all tests

```
make test
```

## Shutdown environment
```
make stop
```
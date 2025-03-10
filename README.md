# USeR
This is the code repository of USeR, a User Story eReviewer.

USeR is a web-based tool that allows authors, such as Product Owners in agile software projects, to assess and optimize user story quality. It implements a user interface for instant, consistent, and explainable user feedback, supporting fast and easy quality optimizations.

USeR was pre-built on a small "demo" German user stories dataset to showcase its behavior. To achieve optimal results, it is recommended to import larger datasets, comprising more than 150 user stories.

## Create a new environment
```
make build
```

## Start the app
```
make up
http://localhost:3000
```

## Adding new projects

1. Define a project identifier(s), e.g., p2 in ./api/config/default.cfg. Multiple projects are possible, separated by a comma (,).

```
[app]
projects = p1,p2
```

2. Add the project identifier(s) in ./web/src/config.json and change the default project if preferred.

```
"projects": [
    {
      "key":"p1"
      "default":true
    },
    {
      "key":"p2"
    }
  ]
```

3. Provide the raw backlog(s) with the user stories as ./api/importer/p2_backlog_raw.csv.

4. Create a new ./api/importer/p2_importer.py that imports the raw user stories.
The importer can be adapted to import project-specific CSV formats.

5. Import the new p2_importer in the ./api/manage.py.

```
from importer.p2_importer import P2Importer
```

6. Finally, execute

```
make ready
```

## Tests

1. Add the project identifier(s) e.g., p2 in ./api/config/tests.cfg

```
[app]
projects = p1,p2
```

2. Provide the raw test backlog(s) with the user stories as ./api/tests/importer/p2_backlog_raw.csv.

3. Define test classes and cases in ./api/tests/test_*.py e.g., class P2UserTestCase(unittest.TestCase).

4. Run all tests

```
make test
```

## Restart app
```
make restart
```

## Shutdown environment
```
make stop
```
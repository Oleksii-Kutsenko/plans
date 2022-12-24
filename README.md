# Before merge

## Code Analyzers

First, need to install types for libraries

```
mypy --install-types
```

Regular run

```
mypy app
black app
pylint app
vulture app
bandit --configfile .\pyproject.toml -r app
```

## Tests

```
docker-compose -f docker-compose.dev.yml exec web coverage run manage.py test
```

## Coverage

```
docker-compose -f docker-compose.dev.yml exec web coverage html
```

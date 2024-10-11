Comands:

Run the backend container:

```
docker-compose -f docker-compose-dev.yml up -d
```

Recreate database container:

```
docker-compose -f docker-compose-dev.yml run users python manage.py recreate_db
```

Populate the database with some dummy data:
```
docker-compose -f docker-compose-dev.yml run users python manage.py seed
```

Run UnitTest
```
docker-compose docker-compose-dev.yml run users python manage.py test
```


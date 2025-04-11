# Backend

Using FastAPI, SQLAlchemy, and PostgreSQL.

## Database

Intialization of alembic database:

```
alembic init alembic
alembic revision --autogenerate -m "Initial revision"
alembic upgrade head
```

To add a new model:

```
alembic revision --autogenerate -m "Add new model"
alembic upgrade head
```

## Celery

Celery is used to run tasks asynchronously.

## Flower

Flower is used to visualize the Celery tasks.

```
http://localhost:5555/
```


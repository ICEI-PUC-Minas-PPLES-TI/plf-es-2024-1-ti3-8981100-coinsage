# Developer Guide: Using Alembic with FastAPI

### 1. On model creation

Every time you create a model you should register it on [`src/models/db/mg.py`](../src/models/db/mg.py). Ex.:

```python
...
from src.models.db.your_new_model_file import YourNewModelClass

...
```


### 2. Create Migration

Every time you make a change on any database model you should generate a migration.

```bash
alembic revision -m "Commit message with your changes description"
```

This will create a new migration script in the [`src/repository/migrations/versions`](../src/repository/migrations/versions/) directory.

### 3. Apply Migration

Apply the migration to the database to create the initial schema.

```bash
alembic upgrade head
```

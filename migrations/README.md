# Migrations

This directory will contain Alembic migration scripts for the database schema.

## Alembic Setup

1. Initialize Alembic (run once):
   alembic init migrations

2. Edit `alembic.ini` and set your database URL.

3. Edit `env.py` to import your models:
   from app.models.database import Base

4. Generate a migration:
   alembic revision --autogenerate -m "Initial migration"

5. Apply migrations:
   alembic upgrade head 
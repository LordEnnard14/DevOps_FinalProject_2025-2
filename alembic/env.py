from __future__ import annotations

from logging.config import fileConfig
import os
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ------------ Ajuste de rutas para importar "app.*" ------------
# Calcula la raíz del proyecto (donde está alembic.ini)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Añade la raíz al sys.path si no está
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Ahora sí podemos importar Base y models
from app.db import Base  # Base = declarative_base()
import app.models  # Importa para que Alembic "vea" las tablas

# ---------------------------------------------------------------

# This is the Alembic Config object, which provides access
# to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set your target metadata here
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    # SQLite offline: literal_binds=True
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Opcional: activa claves foráneas si usas FKs
        # render_as_batch=True permite ALTER TABLE en SQLite
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Activar PRAGMA foreign_keys=ON para SQLite (si usaras FKs)
        if "sqlite" in str(connection.engine.url):
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # importante en SQLite para ALTER TABLE
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

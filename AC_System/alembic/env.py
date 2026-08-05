import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
import sqlmodel

# Tutaj importuj wszystkie swoje modele z tego mikroserwisu (AC_System)
from app.models.logs import SystemContainerLog

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = sqlmodel.SQLModel.metadata


def include_object(object, name, type_, reflected, compare_to):
    """
    Funkcja filtrująca. Chroni przed ingerencją w tabele z innych mikroserwisów.
    """
    if type_ == "table":
        # 1. Chronimy tabele migracyjne innych serwisów
        if name.startswith("alembic_version"):
            return name == "alembic_version_ac_system"
        
        # 2. Ignorujemy tabele w bazie, których nie ma zdefiniowanych w kodzie tego serwisu.
        # Dzięki temu Alembic nie wygeneruje "DROP TABLE" dla tabel z AB_Auth czy innych.
        if target_metadata is not None and name not in target_metadata.tables:
            return False
            
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table="alembic_version_ac_system",  # Własna tabela wersji dla offline
        include_object=include_object               # Filtrowanie tabel dla offline
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata, 
        user_module_prefix="sqlmodel.sql.sqltypes.",
        version_table="alembic_version_ac_system",  # Własna tabela wersji dla online
        include_object=include_object               # Filtrowanie tabel dla online
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context."""

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config.settings import get_settings
import src.domain.entities
from src.infrastructure.database.base import Base

# Alembic Config object
config = context.config

# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogeneration support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """
    settings = get_settings()

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """
    Execute migrations using an active connection.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """
    settings = get_settings()
    print(settings.DATABASE_URL)
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
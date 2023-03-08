# prettier-ignore
import os
from alembic import context
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from logging.config import fileConfig

import sys
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app'))
sys.path.insert(0, folder)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# if not config.get_main_option('sqlalchemy.url'):
DB_USERNAME: str = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST: str = os.getenv("MYSQL_HOST", "localhost")
DB_PORT: str = os.getenv("MYSQL_PORT", 3306)
DB_DATABASE: str = os.getenv("MYSQL_DATABASE")
config.set_main_option(
    'sqlalchemy.url', f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}')

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# Base = declarative_base()

from db import Base, ENGINE
from model import *
target_metadata = Base.metadata
print(target_metadata)
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    connectable = ENGINE

    with connectable.connect() as connection:
        context.configure(
            url = url,
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

if __name__ == '__main__': 
    print(config)
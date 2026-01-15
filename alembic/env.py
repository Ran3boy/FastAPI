import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- ВАЖНО ---
# Добавляем корень проекта в PYTHONPATH, чтобы Alembic видел пакет "app"
# В контейнере корень проекта: /app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app.models import Base
from app.config import settings

# Alembic Config object
config = context.config

# Настройка логирования (может падать, если в alembic.ini нет секций formatters/handlers)
try:
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)
except Exception:
    # Логи не критичны для миграций в учебном проекте
    pass

# Берём URL из переменных окружения/настроек приложения
config.set_main_option("sqlalchemy.url", settings.database_url)

# Метаданные моделей для автогенерации миграций
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме (с подключением к БД)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

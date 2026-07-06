from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
import os

# Permite importar app/config/models
sys.path.append(os.getcwd())

from config.database import DATABASE_URL, Base
from models.User import User  # importe TODOS seus models aqui
from models.Codigo import Codigo
from models.Plano import Plano
from models.Frota import Frota
from models.CustosAnuais import CustosAnuais
from models.Franquia import Franquia
from models.Franqueado import Franqueado
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Calcao import Calcao
from models.Semanal import Semanal
from models.Oficina import Oficina
from models.Despesa import Despesa
from models.DespesaFixa import DespesaFixa
from models.Multa import Multa
from models.Faturamento import Faturamento
from models.Nota import Nota
from models.Locatario import Locatario
from models.Anexo import Anexo
config = context.config

# Define dinamicamente a URL do banco
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# IMPORTANTE: metadata dos seus models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# atualizar alteracoes no model
# alembic revision --autogenerate -m "campos para imagens"
# atualizar o banco
# alembic upgrade head
# uvicorn main:app   --host 0.0.0.0   --port 8001   --log-level debug
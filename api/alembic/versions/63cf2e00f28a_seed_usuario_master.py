"""seed usuario master

Revision ID: 63cf2e00f28a
Revises: ab4d96800968
Create Date: 2026-09-15 20:32:24.195873

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = "def456"
down_revision = "ab4d96800968"
branch_labels = None
depends_on = None


def upgrade():
    users = sa.table(
        "users",
        sa.column("nome", sa.String),
        sa.column("email", sa.String),
        sa.column("password", sa.String),
        sa.column("tipoAcessoID", sa.Integer),
        sa.column("status", sa.Integer),
        sa.column("log_id", sa.Integer),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
        sa.column("deleted_at", sa.DateTime),
    )

    agora = datetime.utcnow()

    op.bulk_insert(
        users,
        [
            {
                "nome": "Master",
                "email": "master@master.com.br",
                "password": "$2b$12$CLWW45GnrH52eAiiviRd2OA5Uj9rWYBLSG9vnSr1B0r9m9U7X5XmG",
                "tipoAcessoID": 1,
                "status": 1,
                "log_id": 0,
                "created_at": agora,
                "updated_at": agora,
                "deleted_at": None,
            },
        ]
    )


def downgrade():
    op.execute("DELETE FROM users WHERE email = 'master@master.com.br'")

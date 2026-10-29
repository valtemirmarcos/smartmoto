"""seed codigos

Revision ID: abc123
Revises: xyz789
Create Date: 2026-09-15
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = "ab4d96800968"
down_revision = "000c073e36a1"
branch_labels = None
depends_on = None


def upgrade():
    codigos = sa.table(
        "codigos",
        sa.column("depara_id", sa.Integer),
        sa.column("codigo", sa.Integer),
        sa.column("descricao", sa.String),
        sa.column("obs", sa.String),
        sa.column("cor", sa.String),
        sa.column("log_id", sa.Integer),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
        sa.column("deleted_at", sa.DateTime),
    )

    op.bulk_insert(
        codigos,
        [
            {"depara_id": 1, "codigo": 2, "descricao": "Invativo", "obs": "AtivoInativo", "cor": None, "log_id": 2, "created_at": datetime(2026, 4, 28, 13, 28, 23), "updated_at": datetime(2026, 5, 11, 18, 11, 46), "deleted_at": None},
            {"depara_id": 1, "codigo": 1, "descricao": "Ativo", "obs": "AtivoInativo", "cor": None, "log_id": 0, "created_at": datetime(2026, 4, 28, 13, 31, 28), "updated_at": datetime(2026, 4, 28, 13, 31, 28), "deleted_at": None},
            {"depara_id": 2, "codigo": 1, "descricao": "Disponivel", "obs": "status frota", "cor": None, "log_id": 0, "created_at": datetime(2026, 5, 5, 20, 43, 7), "updated_at": datetime(2026, 5, 5, 20, 43, 7), "deleted_at": None},
            {"depara_id": 2, "codigo": 2, "descricao": "Alugada", "obs": "status frota", "cor": None, "log_id": 0, "created_at": datetime(2026, 5, 5, 20, 43, 21), "updated_at": datetime(2026, 5, 5, 20, 43, 21), "deleted_at": None},
            {"depara_id": 3, "codigo": 1, "descricao": "Em Aberto", "obs": "Semanais", "cor": "#89CFF0", "log_id": 2, "created_at": datetime(2026, 5, 11, 17, 56, 53), "updated_at": datetime(2026, 5, 11, 17, 56, 53), "deleted_at": None},
            {"depara_id": 3, "codigo": 2, "descricao": "Pago", "obs": "Semanais", "cor": "#28a745", "log_id": 2, "created_at": datetime(2026, 5, 11, 17, 57, 31), "updated_at": datetime(2026, 5, 11, 17, 57, 31), "deleted_at": None},
            {"depara_id": 3, "codigo": 3, "descricao": "Atrasado", "obs": "Semanais", "cor": "#dc3545", "log_id": 2, "created_at": datetime(2026, 5, 11, 17, 57, 57), "updated_at": datetime(2026, 5, 11, 17, 57, 57), "deleted_at": None},
            {"depara_id": 4, "codigo": 1, "descricao": "Ativo", "obs": "Calçoes", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 53, 20), "updated_at": datetime(2026, 5, 13, 17, 53, 20), "deleted_at": None},
            {"depara_id": 4, "codigo": 2, "descricao": "Recolhido", "obs": "Calçoes", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 53, 35), "updated_at": datetime(2026, 5, 13, 17, 53, 35), "deleted_at": None},
            {"depara_id": 4, "codigo": 3, "descricao": "Devolvido", "obs": "Calçoes", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 53, 49), "updated_at": datetime(2026, 5, 13, 17, 53, 49), "deleted_at": None},
            {"depara_id": 5, "codigo": 1, "descricao": "Pix", "obs": "Pagamentos", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 55, 14), "updated_at": datetime(2026, 5, 13, 17, 55, 14), "deleted_at": None},
            {"depara_id": 5, "codigo": 2, "descricao": "Cartão Crédito", "obs": "Pagamentos", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 55, 56), "updated_at": datetime(2026, 5, 13, 17, 55, 56), "deleted_at": None},
            {"depara_id": 5, "codigo": 3, "descricao": "Cartão Débito", "obs": "Pagamentos", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 56, 10), "updated_at": datetime(2026, 5, 13, 17, 56, 10), "deleted_at": None},
            {"depara_id": 5, "codigo": 4, "descricao": "Dinheiro", "obs": "Pagamentos", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 13, 17, 56, 24), "updated_at": datetime(2026, 5, 13, 17, 56, 24), "deleted_at": None},
            {"depara_id": 6, "codigo": 1, "descricao": "Em Aberto", "obs": "Multas", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 17, 39, 33), "updated_at": datetime(2026, 5, 14, 17, 39, 33), "deleted_at": None},
            {"depara_id": 6, "codigo": 2, "descricao": "Processando", "obs": "Multas", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 17, 40, 34), "updated_at": datetime(2026, 5, 14, 17, 40, 34), "deleted_at": None},
            {"depara_id": 6, "codigo": 3, "descricao": "Pago", "obs": "Multas", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 17, 40, 56), "updated_at": datetime(2026, 5, 14, 17, 40, 56), "deleted_at": None},
            {"depara_id": 5, "codigo": 5, "descricao": "Calção", "obs": "Pagamentos", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 17, 45, 37), "updated_at": datetime(2026, 5, 14, 17, 45, 37), "deleted_at": None},
            {"depara_id": 7, "codigo": 1, "descricao": "Franquia", "obs": "Tipo Faturamento", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 19, 15, 16), "updated_at": datetime(2026, 5, 14, 19, 15, 16), "deleted_at": None},
            {"depara_id": 7, "codigo": 2, "descricao": "Calção", "obs": "Tipo Faturamento", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 19, 15, 26), "updated_at": datetime(2026, 5, 14, 19, 15, 26), "deleted_at": None},
            {"depara_id": 7, "codigo": 3, "descricao": "Outro", "obs": "Tipo Faturamento", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 19, 15, 35), "updated_at": datetime(2026, 5, 14, 19, 15, 35), "deleted_at": None},
            {"depara_id": 8, "codigo": 1, "descricao": "Devendo", "obs": "Pgto Faturamento", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 19, 17, 52), "updated_at": datetime(2026, 5, 14, 19, 17, 52), "deleted_at": None},
            {"depara_id": 8, "codigo": 2, "descricao": "Baixado", "obs": "Pgto Faturamento", "cor": None, "log_id": 2, "created_at": datetime(2026, 5, 14, 19, 18, 7), "updated_at": datetime(2026, 5, 14, 19, 18, 7), "deleted_at": None},
            {"depara_id": 9, "codigo": 1, "descricao": "Aberto", "obs": "Status Custo", "cor": None, "log_id": 2, "created_at": datetime(2026, 7, 3, 19, 29, 43), "updated_at": datetime(2026, 7, 3, 19, 29, 43), "deleted_at": None},
            {"depara_id": 9, "codigo": 2, "descricao": "Pago", "obs": "Status Custo", "cor": None, "log_id": 2, "created_at": datetime(2026, 7, 3, 19, 29, 53), "updated_at": datetime(2026, 7, 3, 19, 29, 53), "deleted_at": None},
        ]
    )


def downgrade():
    op.execute("""
        DELETE FROM codigos WHERE
        (depara_id, codigo) IN (
            (1,2),(1,1),(2,1),(2,2),(3,1),(3,2),(3,3),
            (4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(5,4),
            (6,1),(6,2),(6,3),(5,5),(7,1),(7,2),(7,3),
            (8,1),(8,2),(9,1),(9,2)
        )
    """)
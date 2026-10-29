"""multas obs"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '8aa30295dc8b'
down_revision: Union[str, Sequence[str], None] = 'e0f928bd91be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'multas',
        sa.Column('obs', sa.String(length=1000), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('multas', 'obs')
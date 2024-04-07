"""Add current_price column to analysis_currency_stage_one table

Revision ID: 47ff9545664d
Revises: b846d6496938
Create Date: 2024-04-07 15:57:26.355355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ff9545664d'
down_revision: Union[str, None] = 'b846d6496938'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('analysis_currency_stage_one', sa.Column('current_price', sa.Float))


def downgrade():
    op.drop_column('analysis_currency_stage_one', 'current_price')
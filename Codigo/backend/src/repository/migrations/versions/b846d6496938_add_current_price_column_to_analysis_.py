"""Add current_price column to analysis_currency_stage_one table

Revision ID: b846d6496938
Revises: 
Create Date: 2024-04-07 15:33:37.115572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b846d6496938'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

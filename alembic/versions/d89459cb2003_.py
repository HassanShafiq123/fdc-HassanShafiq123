"""empty message

Revision ID: d89459cb2003
Revises: 90048013bd34
Create Date: 2024-04-15 22:06:39.506890

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d89459cb2003"
down_revision: Union[str, None] = "90048013bd34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("menu", "category_id", new_column_name="category")
    op.alter_column("menu", "restraunt_id", new_column_name="restraunt")


def downgrade() -> None:
    pass

"""create tables

Revision ID: 90048013bd34
Revises: 
Create Date: 2024-04-15 21:38:11.281669

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "90048013bd34"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "restraunt",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(300)),
    )
    op.create_table(
        "category",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(300)),
    )
    op.create_table(
        "menu",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(300)),
        sa.Column("ingredients", sa.Text),
        sa.Column("allergens", sa.Text),
        sa.Column("picture", sa.Text, nullable=True),
        sa.Column("category_id", sa.Integer, nullable=True),
        sa.Column("restraunt_id", sa.Integer, nullable=True),
    )
    op.create_foreign_key("fk_menu_category", "menu", "category", ["category_id"], ["id"])
    op.create_foreign_key(
        "fk_menu_restraunt", "menu", "restraunt", ["restraunt_id"], ["id"]
    )


def downgrade() -> None:
    pass

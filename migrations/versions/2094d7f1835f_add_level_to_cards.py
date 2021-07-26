"""Add level to cards.

Revision ID: 2094d7f1835f
Revises: f9490b88266b
Create Date: 2021-07-25 18:39:55.681457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2094d7f1835f'
down_revision = 'f9490b88266b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("cards", schema=None) as batch_op:
        batch_op.add_column(sa.Column("level", sa.Integer(), nullable=False))
        batch_op.create_index("ix_cards_level", ["type"], unique=False)


def downgrade():
    with op.batch_alter_table("cards", schema=None) as batch_op:
        batch_op.drop_index("level")
        batch_op.drop_column("ix_cards_level")

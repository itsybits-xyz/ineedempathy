"""🃏 Modify Cards: Add display name and definition attributes.

Revision ID: cde071912d0a
Revises: 6eb2ce49d533
Create Date: 2021-07-30 09:41:02.803620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cde071912d0a'
down_revision = '6eb2ce49d533'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cards', sa.Column('display_name', sa.String()))
    op.add_column('cards', sa.Column('definition', sa.String()))
    op.add_column('cards', sa.Column('definition_source', sa.String()))


def downgrade():
    op.drop_column('cards', 'display_name')
    op.drop_column('cards', 'definition')
    op.drop_column('cards', 'definition_source')

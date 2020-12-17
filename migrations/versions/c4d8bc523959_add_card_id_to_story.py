"""Add card_id to Story

Revision ID: c4d8bc523959
Revises: 53288d545c7d
Create Date: 2020-12-17 14:15:24.605356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4d8bc523959'
down_revision = '53288d545c7d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('card_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('story_card_id'), ['cards.id'])


def downgrade():
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('story_card_id'))
        batch_op.drop_column('card_id')

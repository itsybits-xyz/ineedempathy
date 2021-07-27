"""Add comments

Revision ID: b011e6be7cf7
Revises: 2094d7f1835f
Create Date: 2021-07-26 16:39:28.410704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b011e6be7cf7'
down_revision = '2094d7f1835f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.Enum('NEED_MET', 'NEET_NOT_MET', 'DEFINE', 'THINK', name='type'), nullable=False),
                    sa.Column('card_id', sa.Integer(), nullable=True),
                    sa.Column('data', sa.Text(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['card_id'], ['cards.id']))
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_comments_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_comments_type'), ['type'], unique=False)
        batch_op.create_index(batch_op.f('ix_comments_card_id'), ['card_id'], unique=False)


def downgrade():
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_comments_id'))
        batch_op.drop_index(batch_op.f('ix_comments_type'))
        batch_op.drop_index(batch_op.f('ix_comments_card_id'))

    op.drop_table('comments')

"""add content column to posts table'

Revision ID: 6de1e3e99387
Revises: 672441108001
Create Date: 2022-02-13 20:15:11.302292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6de1e3e99387'
down_revision = '672441108001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

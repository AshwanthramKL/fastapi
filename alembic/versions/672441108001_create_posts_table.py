"""create posts table

Revision ID: 672441108001
Revises: 
Create Date: 2022-02-13 19:13:41.578951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '672441108001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass

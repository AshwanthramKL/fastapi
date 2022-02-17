"""add few more columns to post table

Revision ID: 895eeb27eaed
Revises: 1dfeb22f3184
Create Date: 2022-02-14 00:47:03.989649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895eeb27eaed'
down_revision = '1dfeb22f3184'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

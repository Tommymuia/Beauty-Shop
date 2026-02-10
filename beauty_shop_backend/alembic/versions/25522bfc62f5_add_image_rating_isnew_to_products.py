"""add_image_rating_isnew_to_products

Revision ID: 25522bfc62f5
Revises: 82513317fea2
Create Date: 2026-02-09 11:29:29.365065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25522bfc62f5'
down_revision: Union[str, Sequence[str], None] = '82513317fea2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('image', sa.String(), nullable=True))
    op.add_column('products', sa.Column('rating', sa.Float(), nullable=False, server_default='4.5'))
    op.add_column('products', sa.Column('is_new', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'is_new')
    op.drop_column('products', 'rating')
    op.drop_column('products', 'image')

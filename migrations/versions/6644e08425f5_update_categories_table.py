"""Update Categories table

Revision ID: 6644e08425f5
Revises: 92c2111bf9b4
Create Date: 2018-04-08 15:07:32.887621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6644e08425f5'
down_revision = '92c2111bf9b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('is_locked', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'is_locked')
    # ### end Alembic commands ###

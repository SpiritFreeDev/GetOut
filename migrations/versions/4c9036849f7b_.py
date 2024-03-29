"""empty message

Revision ID: 4c9036849f7b
Revises: 
Create Date: 2018-03-25 14:24:56.923125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c9036849f7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('cat_name', sa.String(length=60), nullable=True),
    sa.Column('subcat_name', sa.String(length=60), nullable=True),
    sa.Column('cat_description', sa.String(length=500), nullable=True),
    sa.Column('subcat_description', sa.String(length=500), nullable=True),
    sa.Column('catregister_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('last_update', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('cat_id'),
    sa.UniqueConstraint('cat_name'),
    sa.UniqueConstraint('subcat_name')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=False),
    sa.Column('last_name', sa.String(length=60), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('register_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_emp_update', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_sysadmin', sa.Boolean(), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('temporary_pwd', sa.Boolean(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('catsubs',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cat_id'], ['categories.cat_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('catsubs')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###

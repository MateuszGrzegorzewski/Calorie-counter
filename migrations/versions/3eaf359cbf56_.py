"""empty message

Revision ID: 3eaf359cbf56
Revises: 
Create Date: 2022-11-05 09:11:13.091442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eaf359cbf56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blocklist_jti'), 'blocklist', ['jti'], unique=False)
    op.create_table('groceries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('foodstuff', sa.String(length=100), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('foodstuff')
    )
    op.create_table('meals_favourite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mealtimes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=100), nullable=False),
    sa.Column('mealtime', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('time',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('products_to_favourite_meal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('favmeal_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favmeal_id'], ['meals_favourite.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['groceries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products_to_mealtimes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_of_meal', sa.String(length=100), nullable=False),
    sa.Column('name_of_meal', sa.String(length=100), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['groceries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products_to_mealtimes')
    op.drop_table('products_to_favourite_meal')
    op.drop_table('users')
    op.drop_table('time')
    op.drop_table('mealtimes')
    op.drop_table('meals_favourite')
    op.drop_table('groceries')
    op.drop_index(op.f('ix_blocklist_jti'), table_name='blocklist')
    op.drop_table('blocklist')
    # ### end Alembic commands ###

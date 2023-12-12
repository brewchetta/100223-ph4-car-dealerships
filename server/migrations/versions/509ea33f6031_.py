"""empty message

Revision ID: 509ea33f6031
Revises: 
Create Date: 2023-12-12 10:18:12.347431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '509ea33f6031'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dealerships_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('owners_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('make', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('date_sold', sa.DateTime(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('dealership_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dealership_id'], ['dealerships_table.id'], name=op.f('fk_cars_table_dealership_id_dealerships_table')),
    sa.ForeignKeyConstraint(['owner_id'], ['owners_table.id'], name=op.f('fk_cars_table_owner_id_owners_table')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cars_table')
    op.drop_table('owners_table')
    op.drop_table('dealerships_table')
    # ### end Alembic commands ###
"""empty message

Revision ID: c49302efcded
Revises: 1fff491841c6
Create Date: 2016-09-28 11:20:05.060777

"""

# revision identifiers, used by Alembic.
revision = 'c49302efcded'
down_revision = '1fff491841c6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('company_employee', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('company_manager', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'company_manager')
    op.drop_column('users', 'company_employee')
    ### end Alembic commands ###
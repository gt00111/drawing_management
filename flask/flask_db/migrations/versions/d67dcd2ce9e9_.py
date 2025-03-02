"""empty message

Revision ID: d67dcd2ce9e9
Revises: 
Create Date: 2025-02-24 21:38:08.327023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd67dcd2ce9e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('administrator', sa.String(length=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'administrator')
    # ### end Alembic commands ###

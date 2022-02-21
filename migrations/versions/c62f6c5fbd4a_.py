"""empty message

Revision ID: c62f6c5fbd4a
Revises: 7f0c22331c32
Create Date: 2022-02-21 16:40:00.488934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c62f6c5fbd4a'
down_revision = '7f0c22331c32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('court', sa.Column('time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('court', 'time')
    # ### end Alembic commands ###
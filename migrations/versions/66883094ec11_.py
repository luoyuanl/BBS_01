"""empty message

Revision ID: 66883094ec11
Revises: c7fb689a905b
Create Date: 2019-07-31 16:24:37.299863

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '66883094ec11'
down_revision = 'c7fb689a905b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bbs_user', sa.Column('uisadmin', sa.Boolean(), nullable=True))
    op.alter_column('bbs_user', 'upassword',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bbs_user', 'upassword',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
    op.drop_column('bbs_user', 'uisadmin')
    # ### end Alembic commands ###

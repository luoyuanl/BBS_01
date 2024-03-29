"""empty message

Revision ID: b6bd8971550d
Revises: 15fd30a9229d
Create Date: 2019-07-30 13:34:48.190628

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b6bd8971550d'
down_revision = '15fd30a9229d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bbs_category', sa.Column('lastpostname', sa.String(length=200), nullable=True))
    op.add_column('bbs_category', sa.Column('lastpostuser', sa.String(length=60), nullable=True))
    op.drop_column('bbs_category', 'clastpost')
    op.alter_column('bbs_user', 'upassword',
               existing_type=mysql.VARCHAR(length=256),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bbs_user', 'upassword',
               existing_type=mysql.VARCHAR(length=256),
               nullable=True)
    op.add_column('bbs_category', sa.Column('clastpost', mysql.VARCHAR(length=200), nullable=True))
    op.drop_column('bbs_category', 'lastpostuser')
    op.drop_column('bbs_category', 'lastpostname')
    # ### end Alembic commands ###

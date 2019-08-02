"""empty message

Revision ID: b1627e1cb6a8
Revises: 7582ea4d34df
Create Date: 2019-08-02 00:37:01.581603

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b1627e1cb6a8'
down_revision = '7582ea4d34df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bbs_category', sa.Column('clastpostname', sa.String(length=200), nullable=True))
    op.add_column('bbs_category', sa.Column('clastreplytime', sa.DATETIME(), nullable=True))
    op.add_column('bbs_category', sa.Column('clastreplyuser', sa.String(length=60), nullable=True))
    op.add_column('bbs_category', sa.Column('compere', sa.String(length=60), nullable=True))
    op.add_column('bbs_category', sa.Column('startdate', sa.DATE(), nullable=True))
    op.drop_column('bbs_category', 'cstartdate')
    op.drop_column('bbs_category', 'lastreplytime')
    op.drop_column('bbs_category', 'lastpostname')
    op.drop_column('bbs_category', 'ccompere')
    op.drop_column('bbs_category', 'lastreplyuser')
    op.add_column('bbs_posts', sa.Column('postuser', sa.String(length=60), nullable=True))
    op.drop_column('bbs_posts', 'puser')
    op.add_column('bbs_replies', sa.Column('replytime', sa.DateTime(), nullable=True))
    op.add_column('bbs_replies', sa.Column('replyuser', sa.String(length=60), nullable=True))
    op.drop_column('bbs_replies', 'rdatetime')
    op.drop_column('bbs_replies', 'rusername')
    op.add_column('bbs_user', sa.Column('birthday', sa.DATE(), nullable=True))
    op.add_column('bbs_user', sa.Column('email', sa.String(length=300), nullable=False))
    op.add_column('bbs_user', sa.Column('gender', sa.Integer(), nullable=True))
    op.add_column('bbs_user', sa.Column('isactive', sa.Boolean(), nullable=True))
    op.add_column('bbs_user', sa.Column('lastlogintime', sa.DATETIME(), nullable=True))
    op.add_column('bbs_user', sa.Column('level', sa.String(length=128), nullable=True))
    op.add_column('bbs_user', sa.Column('money', sa.Integer(), nullable=True))
    op.add_column('bbs_user', sa.Column('nativeplace', sa.String(length=128), nullable=True))
    op.add_column('bbs_user', sa.Column('password', sa.String(length=128), nullable=False))
    op.add_column('bbs_user', sa.Column('photo', sa.String(length=200), nullable=True))
    op.add_column('bbs_user', sa.Column('qqnum', sa.String(length=15), nullable=True))
    op.add_column('bbs_user', sa.Column('realname', sa.String(length=60), nullable=True))
    op.add_column('bbs_user', sa.Column('regtime', sa.DATETIME(), nullable=True))
    op.add_column('bbs_user', sa.Column('safeanswer', sa.String(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('safequestion', sa.String(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('score', sa.Integer(), nullable=True))
    op.add_column('bbs_user', sa.Column('signature', sa.String(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('type', sa.String(length=60), nullable=True))
    op.drop_column('bbs_user', 'uisactive')
    op.drop_column('bbs_user', 'usafequestion')
    op.drop_column('bbs_user', 'uemail')
    op.drop_column('bbs_user', 'usignature')
    op.drop_column('bbs_user', 'uscore')
    op.drop_column('bbs_user', 'uregtime')
    op.drop_column('bbs_user', 'ubirthday')
    op.drop_column('bbs_user', 'ulevel')
    op.drop_column('bbs_user', 'ustatus')
    op.drop_column('bbs_user', 'uphoto')
    op.drop_column('bbs_user', 'ugender')
    op.drop_column('bbs_user', 'umoney')
    op.drop_column('bbs_user', 'usafeanswer')
    op.drop_column('bbs_user', 'urealname')
    op.drop_column('bbs_user', 'unativeplace')
    op.drop_column('bbs_user', 'uqqnum')
    op.drop_column('bbs_user', 'upassword')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bbs_user', sa.Column('upassword', mysql.VARCHAR(length=256), nullable=False))
    op.add_column('bbs_user', sa.Column('uqqnum', mysql.VARCHAR(length=15), nullable=True))
    op.add_column('bbs_user', sa.Column('unativeplace', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('bbs_user', sa.Column('urealname', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('bbs_user', sa.Column('usafeanswer', mysql.VARCHAR(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('umoney', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('bbs_user', sa.Column('ugender', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('bbs_user', sa.Column('uphoto', mysql.VARCHAR(length=200), nullable=True))
    op.add_column('bbs_user', sa.Column('ustatus', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('bbs_user', sa.Column('ulevel', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('bbs_user', sa.Column('ubirthday', sa.DATE(), nullable=True))
    op.add_column('bbs_user', sa.Column('uregtime', mysql.DATETIME(), nullable=True))
    op.add_column('bbs_user', sa.Column('uscore', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('bbs_user', sa.Column('usignature', mysql.VARCHAR(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('uemail', mysql.VARCHAR(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('usafequestion', mysql.VARCHAR(length=300), nullable=True))
    op.add_column('bbs_user', sa.Column('uisactive', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('bbs_user', 'type')
    op.drop_column('bbs_user', 'signature')
    op.drop_column('bbs_user', 'score')
    op.drop_column('bbs_user', 'safequestion')
    op.drop_column('bbs_user', 'safeanswer')
    op.drop_column('bbs_user', 'regtime')
    op.drop_column('bbs_user', 'realname')
    op.drop_column('bbs_user', 'qqnum')
    op.drop_column('bbs_user', 'photo')
    op.drop_column('bbs_user', 'password')
    op.drop_column('bbs_user', 'nativeplace')
    op.drop_column('bbs_user', 'money')
    op.drop_column('bbs_user', 'level')
    op.drop_column('bbs_user', 'lastlogintime')
    op.drop_column('bbs_user', 'isactive')
    op.drop_column('bbs_user', 'gender')
    op.drop_column('bbs_user', 'email')
    op.drop_column('bbs_user', 'birthday')
    op.add_column('bbs_replies', sa.Column('rusername', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('bbs_replies', sa.Column('rdatetime', mysql.DATETIME(), nullable=True))
    op.drop_column('bbs_replies', 'replyuser')
    op.drop_column('bbs_replies', 'replytime')
    op.add_column('bbs_posts', sa.Column('puser', mysql.VARCHAR(length=60), nullable=True))
    op.drop_column('bbs_posts', 'postuser')
    op.add_column('bbs_category', sa.Column('lastreplyuser', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('bbs_category', sa.Column('ccompere', mysql.VARCHAR(length=20), nullable=True))
    op.add_column('bbs_category', sa.Column('lastpostname', mysql.VARCHAR(length=200), nullable=True))
    op.add_column('bbs_category', sa.Column('lastreplytime', mysql.DATETIME(), nullable=True))
    op.add_column('bbs_category', sa.Column('cstartdate', sa.DATE(), nullable=True))
    op.drop_column('bbs_category', 'startdate')
    op.drop_column('bbs_category', 'compere')
    op.drop_column('bbs_category', 'clastreplyuser')
    op.drop_column('bbs_category', 'clastreplytime')
    op.drop_column('bbs_category', 'clastpostname')
    # ### end Alembic commands ###
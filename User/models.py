# 创建模型
from datetime import datetime

from ext import db


class BaseModel():
    # 保存单条记录
    def save_one(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    # 保存多条记录
    @staticmethod
    def save_all(objlist):
        try:
            db.session.add_all(objlist)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    # 删除单条记录
    def delete_one(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False


# 创建用户模型
class User(db.Model, BaseModel):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    upassword_hash = db.Column(db.String(128), nullable=False)
    uemail = db.Column(db.String(300))
    # 安全问题
    usafequestion = db.Column(db.Integer)
    usafeanswer = db.Column(db.String(300))
    ugender = db.Column(db.Integer, default=0)
    ubirthday = db.Column(db.DATE)
    urealname = db.Column(db.String(60), nullable=True)
    unativeplace = db.Column(db.Integer)
    uqqnum = db.Column(db.String(15))
    # 头像，存路径
    uportrait = db.Column(db.String(200), default='')
    usignature = db.Column(db.String(300))
    umoney = db.Column(db.Integer)
    uscore = db.Column(db.Integer)
    uregtime = db.Column(db.DATETIME)
    uisactive = db.Column(db.Boolean, default=False)
    __tablename__ = 'bbs_user'

    def __str__(self):
        return self.username + '___' + self.password_hash


class Category(db.Model, BaseModel):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryname = db.Column(db.String(100), unique=True, nullable=False)
    cpid = db.Column(db.Integer, default=False, nullable=False)
    cthemecount = db.Column(db.Integer, default=0)
    creplycount = db.Column(db.Integer, default=0)
    clastpost = db.Column(db.String(200))
    ccompere = db.Column(db.String(60), db.ForeignKey('bbs_user.username',onupdate='CASCADE',ondelete='CASECADE'))
    cstartdate = db.Column(db.DATE)
    cpost = db.relationship('Posts', backref='category', lazy='dynamic', cascade='delete')
    __tablename__ = 'bbs_category'

    # 获取所有大板块
    @classmethod
    def all_big(cls):
        return cls.query.filter(cls.pid == 0)

    # 根据cid的值获取大小板块
    @classmethod
    def big_and_small(cls, cid=0):
        if cid == 0:
            bigs = cls.all_big()
            smalls = cls.query.filter(cls.pid != 0)
        else:
            bigs = cls.query.filter(cls.cid == cid)
            smalls = cls.query.filter(cls.pid == cid)
        return bigs, smalls


class Posts(db.Model, BaseModel):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ptitle = db.Column(db.String(200), nullable=False)
    pcontent = db.Column(db.String(20000))
    pposttime = db.Column(db.DateTime, default=datetime.now)
    pistop = db.Column(db.Boolean, default=False)
    pislight = db.Column(db.Boolean, default=False)
    piselite = db.Column(db.Boolean, default=False)
    pisdel = db.Column(db.Boolean, default=False)
    phits = db.Column(db.Integer, default=0)
    preplycount = db.Column(db.Integer, default=0)
    plastreplyid = db.Column(db.Integer, db.ForeignKey('bbs_user.uid'))
    plastreplytime = db.Column(db.DateTime)
    pprice = db.Column(db.Integer)
    puid = db.Column(db.Integer, db.ForeignKey('bbs_user.uid'))
    pcid = db.Column(db.Integer, db.ForeignKey('bbs_category.cid'), nullable=False, default=3)
    __tablename__ = 'bbs_posts'

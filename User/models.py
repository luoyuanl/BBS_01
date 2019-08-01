# 创建模型
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    __tablename__ = 'bbs_user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    upassword = db.Column(db.String(128), nullable=False)
    uemail = db.Column(db.String(300))
    usafequestion = db.Column(db.String(300))
    usafeanswer = db.Column(db.String(300))
    ugender = db.Column(db.Integer, default=0)
    ubirthday = db.Column(db.DATE)
    urealname = db.Column(db.String(60), nullable=True)
    unativeplace = db.Column(db.String(128))
    uqqnum = db.Column(db.String(15))
    uphoto = db.Column(db.String(200), default='/static/images/avatar_blank')
    usignature = db.Column(db.String(300))
    umoney = db.Column(db.Integer,default=50)
    uscore = db.Column(db.Integer,default=50)
    ustatus = db.Column(db.String(60),default='游客')
    ulevel = db.Column(db.String(128),default='小学生')
    uregtime = db.Column(db.DATETIME,default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    uisactive = db.Column(db.Boolean, default=False)

    def login(self):
        self.umoney += 10
        self.uscore += 1
        self.save_one()

    def editpost(self):
        # 发帖加50金币，5积分
        self.umoney += 50
        self.uscore += 5
        self.save_one()

    def replypost(self):
        self.umoney += 10
        self.uscore += 2
        self.save_one()


class Category(db.Model, BaseModel):
    __tablename__ = 'bbs_category'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryname = db.Column(db.String(100), unique=True, nullable=False)
    cpid = db.Column(db.Integer, default=False, nullable=False)
    cthemecount = db.Column(db.Integer, default=0)
    creplycount = db.Column(db.Integer, default=0)
    ccompere = db.Column(db.String(60))
    cstartdate = db.Column(db.DATE,default=datetime.today())
    lastpostname = db.Column(db.String(200))
    lastreplyuser = db.Column(db.String(60))
    lastreplytime = db.Column(db.DATETIME)

    def editpost(self,username):
        self.cthemecount += 1
        self.lastpostname = username
        self.save_one()

    def replypost(self,username):
        self.creplycount +=1
        self.lastreplytime=datetime.now()
        self.lastreplyuser = username
        self.save_one()

    # 获取所有大板块
    @classmethod
    def get_big(cls):
        return cls.query.filter(cls.cpid == 0)

    # 根据cid的值获取大小板块
    @classmethod
    def big_and_small(cls, cid=0):
        if cid == 0:
            bigs = cls.get_big().all()
            smalls = cls.query.filter(cls.cpid != 0).all()
        else:
            bigs = cls.query.filter(cls.cid == cid).all()
            smalls = cls.query.filter(cls.cid == cid).all()
        return bigs, smalls


class Posts(db.Model, BaseModel):
    __tablename__ = 'bbs_posts'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ptitle = db.Column(db.String(200), nullable=False)
    pcontent = db.Column(db.String(20000))
    pposttime = db.Column(db.DateTime, default=datetime.now())
    pistop = db.Column(db.Boolean, default=False)
    pislight = db.Column(db.Boolean, default=False)
    piselite = db.Column(db.Boolean, default=False)
    pisdel = db.Column(db.Boolean, default=False)
    phits = db.Column(db.Integer, default=0)
    preplycount = db.Column(db.Integer, default=0)
    plastreplyuser = db.Column(db.String(60))
    plastreplytime = db.Column(db.DateTime)
    pprice = db.Column(db.Integer,default=0)
    puser = db.Column(db.String(60))
    pcid = db.Column(db.Integer, nullable=False, default=3)

    def replypost(self,username,replytime):
        self.preplycount +=1
        self.plastreplyuser = username
        self.plastreplytime = replytime
        self.save_one()


class Replies(db.Model, BaseModel):
    __tablename__ = 'bbs_replies'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rcontent = db.Column(db.String(20000), nullable=False)
    rfloor = db.Column(db.Integer, autoincrement=True)
    rdatetime = db.Column(db.DateTime,default=datetime.now())
    rpid = db.Column(db.Integer, db.ForeignKey('bbs_posts.pid'), nullable=False)
    rusername = db.Column(db.String(60))



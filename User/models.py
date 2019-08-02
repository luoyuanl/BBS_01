# 创建模型
import hashlib
from datetime import datetime

from flask import session

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
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    safequestion = db.Column(db.String(300), default='None')
    safeanswer = db.Column(db.String(300), default='None')
    gender = db.Column(db.Integer, default=0)  # 0未填写，1男，2女
    birthday = db.Column(db.DATE)
    realname = db.Column(db.String(60))
    nativeplace = db.Column(db.String(128))
    qqnum = db.Column(db.String(15))
    photo = db.Column(db.String(200), default='/static/upload/20190731143342.png')
    signature = db.Column(db.String(300))
    money = db.Column(db.Integer, default=50)
    score = db.Column(db.Integer, default=50)
    type = db.Column(db.String(60), default='游客')  # 游客、版主、管理员
    level = db.Column(db.String(128), default='小学生')
    regtime = db.Column(db.DATETIME, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    isactive = db.Column(db.Boolean, default=False)
    lastlogintime = db.Column(db.DATETIME, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def check_dologin(self, checkinfo):
        if checkinfo.username == self.username and hashlib.sha1(
                (checkinfo.password).encode(
                    'utf8')).hexdigest() == self.password and checkinfo.safequestion == self.safequestion and checkinfo.safeanswer == self.safeanswer:
            return True
        else:
            return False

    def login(self):
        # 登录加2金币,没有判断每日登录
        self.money += 2
        self.save_one()

    def editpost(self):
        # 发帖加5金币，2积分
        self.money += 5
        self.score += 2
        self.save_one()

    def replypost(self):
        # 回帖加2金币，1积分
        self.money += 2
        self.score += 1
        self.save_one()

    def setsession(self):
        # 登陆成功设置session
        session.permanent = True
        session['uid'] = self.uid
        session['username'] = self.username
        session['score'] = self.score
        session['photo'] = self.photo
        session['type'] = self.type
        session['level'] = self.level
        session['signature'] = self.signature


# 创建板块
class Category(db.Model, BaseModel):
    __tablename__ = 'bbs_category'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryname = db.Column(db.String(100), unique=True, nullable=False)
    cpid = db.Column(db.Integer, default=False, nullable=False)
    cthemecount = db.Column(db.Integer, default=0)
    creplycount = db.Column(db.Integer, default=0)
    compere = db.Column(db.String(60))
    startdate = db.Column(db.DATE, default=datetime.today())
    clastpostname = db.Column(db.String(200))
    clastreplyuser = db.Column(db.String(60))
    clastreplytime = db.Column(db.DATETIME)

    def editpost(self, postname):
        self.cthemecount += 1
        self.clastpostname = postname
        self.save_one()

    def replypost(self, username):
        self.creplycount += 1
        self.clastreplytime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.clastreplyuser = username
        self.save_one()


    # 展示板块名称
    @classmethod
    def show_category(cls, cid):
        if cid != 0:
            bigcategories = Category.query.filter(Category.cpid == 0).all()
            smallcategories = Category.query.filter(Category.cpid != 0).all()
            smallc = Category.query.filter(Category.cid == cid).first()
            bigc = Category.query.filter(Category.cid == smallc.cpid).first()

        else:
            bigcategories = Category.query.filter(Category.cpid == 0).all()
            smallcategories=Category.query.filter(Category.cpid != 0).all()
            smallc = None
            bigc = None
        return bigcategories, smallcategories, bigc, smallc


class Posts(db.Model, BaseModel):
    __tablename__ = 'bbs_posts'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ptitle = db.Column(db.String(200), nullable=False)
    pcontent = db.Column(db.String(20000))
    pposttime = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    pistop = db.Column(db.Boolean, default=False)
    pislight = db.Column(db.Boolean, default=False)
    piselite = db.Column(db.Boolean, default=False)
    pisdel = db.Column(db.Boolean, default=False)
    phits = db.Column(db.Integer, default=0)
    preplycount = db.Column(db.Integer, default=0)
    plastreplyuser = db.Column(db.String(60))
    plastreplytime = db.Column(db.DateTime)
    pprice = db.Column(db.Integer, default=0)
    postuser = db.Column(db.String(60))
    pcid = db.Column(db.Integer, nullable=False, default=3)

    def replypost(self, username):
        # 更新帖子列表信息
        self.preplycount += 1
        self.plastreplyuser = username
        self.plastreplytime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_one()


class Replies(db.Model, BaseModel):
    __tablename__ = 'bbs_replies'
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rcontent = db.Column(db.String(20000), nullable=False)
    rpid = db.Column(db.Integer, db.ForeignKey('bbs_posts.pid'), nullable=False)
    isshielded = db.Column(db.Boolean, default=False)
    replytime = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    replyuser = db.Column(db.String(60))

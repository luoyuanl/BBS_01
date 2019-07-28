from flask import Blueprint, render_template
from ext import db
from User.models import *
from User.views import bbs


# 创建表
@bbs.route('/create/')
def create_table():
    db.create_all()
    return 'create_all'


# 删除表
@bbs.route('/drop/')
def delete_tables():
    db.drop_all()
    return 'drop_all'


# 增加一条记录
@bbs.route('/add1/')
def add_user():
    # user = User()
    # user.username = 'admin'
    # # user.upassword_hash = hashlib.sha1(b'123').hexdigest()
    # user.upassword_hash = '123'
    # user.save_one()
    # return 'add_user'
    category = Category()
    category.categoryname = 'python'
    category.cpid = 2
    category.save_one()
    return 'add_category'


# 删除一条记录
@bbs.route("/delete/<int:uid>/")
def delete_user(uid):
    user = User.query.get(uid)
    User.query.all()
    user.delete()
    return "delete_user"


# 修改
@bbs.route('/update/<int:uid>/')
def update_user(uid):
    # 查询指定pk（主键）的记录
    # user必须是User的对象才能修改
    user = User.query.get(uid)
    if user:
        user.username = '哈哈哈'
        db.session.add(user)
        db.session.commit()
    print(user, type(user))
    return "修改记录"


@bbs.route('/jiangxiaomeng/')
def create_all():
    user1 = User(username='admin', upassword_hash='123')
    user2 = User(username='张三', upassword_hash='456')
    user3 = User(username='李四', upassword_hash='lisi')
    cat1 = Category(categoryname='python基础', cpid=0)
    cat2 = Category(categoryname='python进阶', cpid=0)
    cat3 = Category(categoryname='python之禅', cpid=0)
    cat1_1 = Category(categoryname='基本语法', cpid=1)
    cat1_2 = Category(categoryname='linux使用', cpid=1)
    cat2_1 = Category(categoryname='flask框架', cpid=2)
    cat2_2 = Category(categoryname='Django框架', cpid=2)
    cat3_3 = Category(categoryname='人生感悟', cpid=3)
    post1 = Posts(ptitle='11111')
    post2 = Posts(ptitle='22222')
    objlist = [user1, user2, user3, cat1, cat2, cat3, cat1_1, cat1_2, cat2_1, cat2_2, cat3_3, post1, post2]
    for i in objlist:
        i.save_one()
    return 'save_all'




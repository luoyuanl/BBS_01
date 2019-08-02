from flask import current_app
from flask_mail import Message
import hashlib
from User.views import *

# 创建表
from ext import mail


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
    user = User()
    user.username = 'admin'
    user.upassword_hash = hashlib.sha1(b'123').hexdigest()
    # user.upassword_hash = '123'
    user.save_one()
    return 'add_user'
    # category = Category()
    # category.categoryname = 'python'
    # category.cpid = 2
    # category.save_one()
    # return 'add_category'


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

@bbs.route('/getmsg/')
def getmsg():
    data = User.query.filter(User.username == '张三').all()
    if data:
        print(data[0].username)
    else:
        print('没有数据')
    return 'found'


@bbs.route('/mailto/')
def mailto():
    # 生成邮件内容
    message = Message('测试', recipients='luoyuan_p@hotmail.com', sender=current_app.config['MAIL_USERNAME'])

    message.html = '<h2>好难！</2>'
    mail.send(message)
    return '发送邮件成功'

@bbs.route('/user/<int:page>')
def list_user(page):
    paginagtion = User.query.paginatate(page=page,per_page=5)
    return render_template('posts,html',**{
        'users':paginagtion.items,
        'current':paginagtion.page,
        'per_page':5
    })

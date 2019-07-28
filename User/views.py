from flask import Blueprint, render_template, request, redirect, make_response, url_for
from ext import db
from User.models import *

# 实例化蓝图
bbs = Blueprint('bbs', __name__, url_prefix='')


@bbs.route('/index/')
@bbs.route('/index/<int:cid>')
def index(cid=0):
    categories = Category.query.filter(Category.cpid == 0).all()
    if cid == 0:
        bigcategory = categories
    else:
        bigcategory = Category.query.filter(Category.cid == cid).all()
    smallcategory = Category.query.filter(Category.cpid != 0).all()

    return render_template('index.html', title='首页', **locals())


# @bbs.route('/login/')
# def user_login():
#     return render_template('login.html')


# cookies
@bbs.route('/login/', methods=['GET', 'POST'])
def user_login():
    username_input = request.form.get('username')
    password_input = request.form.get('password')
    # print(username_input, password_input)
    # 验证用户名和密码是否正确
    data = User.query.filter(User.username == username_input).all()
    if data:
        user = User.query.filter(User.username == username_input, User.upassword_hash == password_input).all()
        if user:
            response = make_response('<script>window.location.href="/index"</script>')
            # response = make_response(render_template('App/index.html'))
            response.set_cookie('username', username_input, max_age=3 * 24 * 3600)
            return response
        else:
            # 验证错误，重新验证
            return '用户名密码错误'
        # return redirect(url_for('bbs.user_login'))
    else:
        return '用户不存在'


@bbs.route('/register/', methods=['GET', 'POST'])
def user_register():
    username_input = request.form.get('username')
    password_input = request.form.get('password')
    email_input = request.form.get('mail')
    user = User(username=username_input, upassword_hash=password_input, uemail=email_input)
    user.save_one()
    # return render_template('register.html',title='注册')


@bbs.route('/logout/')
def user_logout():
    response = make_response('<script>window.location.href="/index/"</script>')
    response.delete_cookie('username')
    return response


#
# @bbs.route('/postslist/')
# @bbs.route('/postlist/<int:cid>')
# def postlist(cid=0):
#     category = Category(cid)
#     return render_template('index.html', title=category.categoryname, **locals())

@bbs.route('/getmsg/')
def getmsg():
    data = User.query.filter(User.username == '张三').all()
    if data:
        print(data[0].username)
    else:
        print('没有数据')
    return 'found'

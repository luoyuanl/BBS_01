import os
from datetime import datetime, timedelta
import hashlib
from datetime import timedelta

from flask import Blueprint, render_template, request, redirect, make_response, url_for, session, g

from User.verifycode import VerifyCode
from ext import db, photos
from User.models import *
from User.verify_reg import RegisterForm
from User.verifycode import VerifyCode

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
    posts = Posts.query.filter(Category.cid == cid).all()
    postscount = db.session.query(Posts).count()
    userscount = db.session.query(User).count()
    newuser = User.query.order_by(User.uid).all()
    return render_template('index.html', title='首页', **locals())


# 登录
@bbs.route('/login/', methods=['GET', 'POST'])
def user_login():
    username_input = request.form.get('username')
    password = request.form.get('password')
    password_input = hashlib.sha1(password.encode('utf8')).hexdigest()
    # 验证用户名和密码是否正确
    users = User.query.filter(User.username == username_input).all()
    if users:
        user = User.query.filter(User.username == username_input, User.upassword == password_input).first()
        if users:
            response = make_response('<script>window.location.href="/index/"</script>')
            session.permanent = True
            # 获取用户信息，存入session
            session['username'] = user.username
            session['uscore'] = user.uscore
            session['uphoto'] = user.uphoto
            session['ustatus'] = user.ustatus
            categories = Category.query.filter(Category.cpid == 0).all()
            # return render_template('index.html', title='首页',**locals())
            return response
        else:
            # 验证错误，重新验证
            return redirect(url_for('bbs.user_login'))
    return redirect(url_for('bbs.user_login'))


# 登出
@bbs.route('/logout/')
def user_logout():
    # 登出时清除session
    response = make_response('<script>window.location.href="/index/"</script>')
    session.clear()
    return response


# 注册
@bbs.route('/register/', methods=['GET', 'POST'])
def user_register():
    # 生成验证表单对象
    registerform = RegisterForm()
    categories = Category.query.filter(Category.cpid == 0).all()
    if request.method == 'POST':
        yzm = request.form.get('yzm')
        code = session.get('code')
        if registerform.validate_on_submit() and yzm == code:
            # 验证成功
            username = registerform.username.data
            password = registerform.passsword.data
            email = registerform.email.data
            user = User(username=username, upassword=hashlib.sha1(password.encode('utf8')).hexdigest(), uemail=email)
            user.save_one()
            return redirect('/register/')
    return render_template('register.html', title='注册', form=registerform, **locals())


# 帖子列表
@bbs.route('/posts/')
@bbs.route('/posts/<int:cid>')
def posts(cid=0):
    categories = Category.query.filter(Category.cpid == 0).all()
    if cid == 0:
        bigcategory = categories
    else:
        bigcategory = Category.query.filter(Category.cid == cid).all()
    smallcategory = Category.query.filter(Category.cpid != 0).all()
    posts = Posts.query.filter(Posts.pcid == cid).all()
    smallc = Category.query.filter(Category.cid == cid).first()
    bigc = Category.query.filter(Category.cid == smallc.cpid).first()
    replies = Replies.query.all()
    return render_template('postlist.html', title='post', **locals())


# 修改密码
@bbs.route('/home_psd/', methods=['GET', 'POST'])
def person_psdsafe():
    categories = Category.query.filter(Category.cpid == 0).all()
    if request.method == 'POST':
        return render_template('home_pwd.html', title='密码安全', **locals())
    else:
        return render_template('home_pwd.html', title='密码安全', **locals())


# 修改个人信息
@bbs.route('/home_info/', methods=['GET', 'POST'])
def person_info():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    if request.method == 'POST':
        user.urealname = request.form.get('realname')
        user.ugender = request.form.get('gender')
        user.ubirthday = request.form.get('birthday')
        user.unativeplace = request.form.get('place')
        user.uqqnum = request.form.get('qq')
        user.save_one()
        return render_template('home_tx.html', title='个人信息', **locals())
    else:
        return render_template('home_person.html', title='个人信息', **locals())


@bbs.route('/home_sign/', methods=['GET', 'POST'])
def person_signature():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    if request.method == 'POST':
        signaure = request.form.get('content')
        return render_template('home_sign.html', title='个人签名', **locals())
    else:
        return render_template('home_sign.html', title='个人签名', **locals())


@bbs.route('/home/', methods=['GET', 'POST'])
def person_protrait():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    img_url = None
    if request.method == 'POST':
        photo = request.files.get('photo')
        if photo:
            filename = photos.save(photo)
            img_url = photos.url(filename)
            user.uphoto = '/static/upload/' + filename
            user.save_one()
    return render_template('home_tx.html', img_url=img_url, categories=categories)


# @bbs.route('/moment/')
# def custom_time():
#     current = datetime.utcnow() + timedelta()
# {{ moment(current_time).fromNow() }}

@bbs.route('/detail/<int:pid>')
def postdetail(pid=1):
    categories = Category.query.filter(Category.cpid == 0).all()
    cid = Posts.query.filter(Posts.pid == pid).first().pcid
    posts = Posts.query.filter(Posts.pcid == cid).all()
    smallc = Category.query.filter(Category.cid == cid).first()
    bigc = Category.query.filter(Category.cid == smallc.cpid).first()
    post = Posts.query.filter(Posts.pid == pid).first()
    replies = Replies.query.filter(Replies.rpid == pid).all()
    postuser = User.query.filter(User.uid == post.puid).first()
    replyuser = User.query.filter(User.uid == Replies.ruid).first()
    return render_template('postdetail.html', **locals())


@bbs.route('/edit/<int:cid>')
def editpost(cid=0):
    smallc = Category.query.filter(Category.cid == cid).first()
    bigc = Category.query.filter(Category.cid == smallc.cpid).first()
    posts = Posts.query.filter(Posts.pcid == cid).all()
    return render_template('editpost.html', **locals())


@bbs.route('/moment/')
def custom_time():
    current = datetime.utcnow()
    return render_template('common/Base.html', current_time=current)


@bbs.route('/upload/', methods=['GET', 'POST'])
def upload():
    img_url = None
    user = ()
    if request.method == 'POST':
        photo = request.files.get('photo')
        if photo:
            filename = photos.save(photo)
            img_url = photos.url(filename)
    return render_template('home_tx.html', img_url=img_url)


# 验证码
@bbs.route('/code/')
def generate_code():
    vc = VerifyCode()
    data = vc.output()
    # 写入session保存验证码字符
    session['code'] = vc.code
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    return response
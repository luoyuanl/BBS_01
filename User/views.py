import os
from datetime import datetime, timedelta
import hashlib
from datetime import timedelta

from flask import Blueprint, render_template, request, redirect, make_response, url_for, session, g

from User import check_login
from User.verifycode import VerifyCode
from ext import db, photos
from User.models import *
from User.verify_reg import RegisterForm
from User.verifycode import VerifyCode

# 实例化蓝图
bbs = Blueprint('bbs', __name__, url_prefix='')


# 首页
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
        if user:
            # 验证成功，用户信息存入session
            session.permanent = True
            session['username'] = user.username
            session['uscore'] = user.uscore
            session['uphoto'] = user.uphoto
            session['ustatus'] = user.ustatus
            categories = Category.query.filter(Category.cpid == 0).all()
            # 登陆成功，转入首页
            return render_template('tmppage.html', picture=1, v='bbs.index', i='登陆成功!', acolor='green', **locals())
        else:
            return render_template('tmppage.html', picture=0, v='bbs.index', i='密码错误，请重新输入', acolor='red', **locals())
    return render_template('tmppage.html', picture=0, v='bbs.index', i='用户名不存在，请先注册', acolor='red', **locals())


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
            return render_template('tmppage.html', picture=1, v='bbs.index', i='注册成功!', acolor='green', **locals())
        return render_template('tmppage.html', picture=0, v='bbs.user_register', i='账号或密码有误，请重新输入', acolor='red',
                               **locals())
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
    username = session.get('username')
    if request.method == 'POST':
        user = User.query.filter(User.username == username).first()
        oldpassword = request.form.get('oldpassword')
        if user.upassword == hashlib.sha1(oldpassword.encode('utf8')).hexdigest():
            password = request.form.get('newpassword')
            password2 = request.form.get('newpassword2')
            if password == password2:
                user.upassword = hashlib.sha1(password.encode('utf8')).hexdigest()
                user.uemail = request.form.get('emailnew')
                user.usafequestion = request.form.get('questionidnew')
                user.usafeanswer = request.form.get('answernew')
                user.save_one()
                print(user.uemail)
                return render_template('tmppage.html', picture=1, v='bbs.person_psdsafe', i='修改密码成功!', acolor='green',
                                       **locals())
            else:
                return render_template('tmppage.html', picture=0, v='bbs.person_psdsafe', i='两次密码输入不一致，请重新输入',
                                       acolor='red',
                                       **locals())
        else:
            return render_template('tmppage.html', picture=0, v='bbs.person_psdsafe', i='旧密码输入错误! 请确认密码', acolor='red',
                                   **locals())
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
        return render_template('tmppage.html', picture=1, v='bbs.person_info', i='修改个人信息成功!', acolor='green',
                               **locals())
    else:
        return render_template('home_person.html', title='个人信息', **locals())


# 修改个性签名
@bbs.route('/home_sign/', methods=['GET', 'POST'])
def person_signature():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    if request.method == 'POST':
        signaure = request.form.get('content')
        return render_template('tmppage.html', picture=1, v='bbs.person_signature', i='修改个性签名成功!', acolor='green',
                               **locals())
    else:
        return render_template('home_sign.html', title='个人签名', **locals())


# 修改头像
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
            return render_template('tmppage.html', picture=1, v='bbs.person_protrait', i='修改头像成功!', acolor='green',
                                   **locals())
        return render_template('tmppage.html', picture=1, v='bbs.person_protrait', i='修改头像失败!请重新常识', acolor='red',
                               **locals())
    return render_template('home_tx.html', **locals())


# 帖子详细信息，回帖
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


# 发帖子
@bbs.route('/edit/<int:cid>', methods=['GET', 'POST'])
def editpost(cid=0):
    smallc = Category.query.filter(Category.cid == cid).first()
    bigc = Category.query.filter(Category.cid == smallc.cpid).first()
    posts = Posts.query.filter(Posts.pcid == cid).all()
    if request.method == 'POST':
        if session.get('username'):
            user = User.query.filter(User.username == session['username']).first()
            title = request.form.get('subject')
            content=request.form.get('')
            puid = user.uid
            # 生成一条帖子记录
            post=Posts(ptitle=title,pcontent=content,puid=puid)
            post.save_one()
            # 更新user信息
            user.editpost()
            # 更新板块信息
            smallc.editpost(user.username)
            thispost=Posts.query.filter(Posts.ptitle==title,Posts.pcontent==content,Posts.puid==user.uid).first()
            return render_template('tmppage.html',picture=1,v='bbs.postdetail',i='发帖成功！获得{}金币和{}积分'.format(user.umoney,user.uscore),acolor='green',pid=thispost.pid,**locals())
        return render_template('tmppage.html',picture=2,v='bbs.index',i='请先登录！',acolor='red',**locals())
    return render_template('editpost.html', **locals())


@bbs.route('/moment/')
def custom_time():
    current = datetime.utcnow()
    return render_template('common/Base.html', current_time=current)


# 上传头像
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

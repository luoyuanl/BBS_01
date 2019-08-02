import hashlib

from flask import Blueprint, render_template, request, session, make_response, url_for

from User.models import User, Category
from User.forms import RegisterForm
from User.verifycode import VerifyCode
from ext import photos

# 实例化user
user = Blueprint('user', __name__, url_prefix='/user')


# 登录
@user.route('/login/', methods=['GET', 'POST'])
def user_login():
    categories = Category.query.filter(Category.cpid == 0).all()
    if request.method == 'POST':
        session['sourcepage'] = request.environ.get('HTTP_REFERER', '/')
        username_input = request.form.get('username')
        password = request.form.get('password')
        # 验证用户名和密码是否正确
        user = User.query.filter(User.username == username_input).first()
        if user:
            if user.password == hashlib.sha1(password.encode('utf8')).hexdigest():
                # 验证成功，用户信息存入session
                # session.permanent = True
                # session['username'] = user.username
                # session['score'] = user.score
                # session['photo'] = user.photo
                # session['type'] = user.type
                # session['level'] = user.level
                user.setsession()
                categories = Category.query.filter(Category.cpid == 0).all()
                # 登陆成功，转入首页
                return render_template('tmppage.html', picture=1, v=url_for('bbs.index'), i='登陆成功!', title='登陆成功',
                                       **locals())
            else:
                return render_template('tmppage.html', picture=0, v=url_for('user.user_login'), i='密码错误，请重新输入',
                                       title='登陆失败', **locals())
        return render_template('tmppage.html', picture=0, v=url_for('user.user_login'), i='用户名不存在，请先注册', title='登陆失败',
                               **locals())
    return render_template('login.html', **locals())


# 登录
@user.route('/dologin/', methods=['GET', 'POST'])
def dologin():
    categories = Category.query.filter(Category.cpid == 0).all()
    code = session.get('code')
    if request.method == 'POST':
        yzm = request.form.get('yzm')
        username_input = request.form.get('username')
        password = request.form.get('password')
        safequestion = request.form.get('safequestion')
        safeanswer = request.form.get('safeanswer')
        user = User.query.filter(User.username == username_input).first()
        if user:
            if user.password == hashlib.sha1(
                    password.encode(
                        'utf8')).hexdigest() and user.safequestion == safequestion and user.safeanswer == safeanswer and yzm == code:
                user.login()
                # 验证成功，用户信息存入session
                user.setsession()
                categories = Category.query.filter(Category.cpid == 0).all()
                # 登陆成功，转入首页
                return render_template('tmppage.html', picture=1, v=url_for('bbs.index'), i='登陆成功!', title='登陆成功',
                                       **locals())
            else:
                return render_template('tmppage.html', picture=0, v=url_for('user.user_login'), i='密码错误，请重新输入',
                                       title='登陆失败', **locals())
        return render_template('tmppage.html', picture=0, v=url_for('user.user_login'), i='用户名不存在，请先注册', title='登陆失败',
                               **locals())
    return render_template('login.html', **locals())


# 登出
@user.route('/logout/')
def user_logout():
    # 登出时清除session
    response = make_response('<script>window.location.href="/index/"</script>')
    session.clear()
    return response


# 注册
@user.route('/register/', methods=['GET', 'POST'])
def user_register():
    # 生成验证表单对象
    registerform = RegisterForm()
    categories = Category.query.filter(Category.cpid == 0).all()
    code = session.get('code')
    if request.method == 'POST':
        yzm = request.form.get('yzm')
        # code = session.get('code')
        if registerform.validate_on_submit() and yzm == code:
            # 验证成功
            session.pop('code')
            username = registerform.username.data
            password = registerform.passsword.data
            email = registerform.email.data
            user = User(username=username, password=hashlib.sha1(password.encode('utf8')).hexdigest(), email=email)
            user.save_one()
            user.setsession()
            # 注册成功，转入首页
            return render_template('tmppage.html', picture=1, v=url_for('bbs.index'), i='注册成功!获得50金币', title='注册成功',
                                   **locals())
        return render_template('tmppage.html', picture=0, v=url_for('user.user_register'), i='账号或密码有误，请重新输入',
                               title='注册失败',
                               **locals())
    return render_template('register.html', title='注册', form=registerform, **locals())


# 注册验证码
@user.route('/code/')
def generate_code():
    vc = VerifyCode()
    data = vc.output()
    # 写入session保存验证码字符
    session['code'] = vc.code
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    return response


# 修改密码
@user.route('/home_psd/', methods=['GET', 'POST'])
def person_psdsafe():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    if request.method == 'POST':
        user = User.query.filter(User.username == username).first()
        oldpassword = request.form.get('oldpassword')
        if user.password == hashlib.sha1(oldpassword.encode('utf8')).hexdigest():
            password = request.form.get('newpassword')
            password2 = request.form.get('newpassword2')
            if password == password2:
                user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
                user.email = request.form.get('emailnew')
                user.safequestion = request.form.get('questionidnew')
                user.safeanswer = request.form.get('answernew')
                user.save_one()
                session.clear()
                return render_template('login.html', title='登录', **locals())
            else:
                return render_template('tmppage.html', picture=0, v=url_for('user.person_psdsafe'), i='两次密码输入不一致，请重新输入',
                                       title='修改密码失败!',
                                       **locals())
        else:
            return render_template('tmppage.html', picture=0, v=url_for('user.person_psdsafe'), i='旧密码输入错误! 请确认密码',
                                   title='修改密码失败!', **locals())
    else:
        return render_template('home_pwd.html', title='密码安全', **locals())


# 修改个人信息
@user.route('/home_info/', methods=['GET', 'POST'])
def person_info():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    if request.method == 'POST':
        user.realname = request.form.get('realname')
        user.gender = request.form.get('gender')
        user.birthday = request.form.get('birthday')
        user.nativeplace = request.form.get('place')
        user.qqnum = request.form.get('qq')
        user.save_one()
        user.setsession()
        return render_template('tmppage.html', picture=1, v=url_for('user.person_info'), i='修改个人信息成功!', **locals())
    else:
        return render_template('home_person.html', title='个人信息', **locals())


# 修改个性签名
@user.route('/home_sign/', methods=['GET', 'POST'])
def person_signature():
    categories = Category.query.filter(Category.cpid == 0).all()
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    if request.method == 'POST':
        user.signature = request.form.get('content')
        user.save_one()
        user.setsession()
        return render_template('tmppage.html', picture=1, v=url_for('user.person_signature'), i='修改个性签名成功!', **locals())
    else:
        return render_template('home_sign.html', title='个人签名', **locals())


# 修改头像
@user.route('/home/', methods=['GET', 'POST'])
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
            user.photo = '/static/upload/' + filename
            session['uphoto'] = user.photo
            user.save_one()
            return render_template('tmppage.html', picture=1, v=url_for('user.person_protrait'), i='修改头像成功!',
                                   **locals())
        return render_template('tmppage.html', picture=1, v=url_for('user.person_protrait'), i='修改头像失败!请重新尝试',
                               **locals())
    return render_template('home_potrait.html', **locals())


# 找回密码
@user.route('/getpass/', methods=['GET', 'POST'])
def getpass():
    categories = Category.query.filter(Category.cpid == 0).all()
    return render_template('')

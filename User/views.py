from flask import Blueprint, render_template, request, redirect, make_response, url_for, session
from User.models import *

# 实例化bbs
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
    bigc = Category.query.filter(Category.cid == cid).first()
    posts = Posts.query.filter(Category.cid == cid).all()
    postscount = db.session.query(Posts).count()
    userscount = db.session.query(User).count()
    newuser = User.query.order_by(User.uid).all()
    return render_template('index.html', title='首页', **locals())


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


# 帖子详细信息、回帖
@bbs.route('/detail/<int:pid>')
@bbs.route('/detail/<int:pid>', methods=['GET', 'POST'])
def postdetail(pid=1):
    categories = Category.query.filter(Category.cpid == 0).all()
    cid = Posts.query.filter(Posts.pid == pid).first().pcid
    posts = Posts.query.filter(Posts.pcid == cid).all()
    smallc = Category.query.filter(Category.cid == cid).first()
    bigc = Category.query.filter(Category.cid == smallc.cpid).first()
    post = Posts.query.filter(Posts.pid == pid).first()
    replies = Replies.query.filter(Replies.rpid == pid).all()
    replylist = []
    for reply in replies:
        replyuser = User.query.filter(User.username == reply.rusername).first()
        replylist.append([reply, replyuser])
    postuser = User.query.filter(User.username == post.puser).first()
    lastreplyuser = User.query.filter(User.username == post.plastreplyuser).first()
    if request.method == 'POST':
        if session.get('username'):
            user = User.query.filter(User.username == session['username']).first()
            myreply = request.form.get('myreply')
            newreply = Replies(rcontent=myreply, rusername=user.username, rpid=post.pid)
            # 生成回复记录
            newreply.save_one()
            # 更新帖子信息
            post.replypost(user.username)
            # 更新user信息
            user.replypost()
            user.setsession()
            # 更新板块信息
            smallc.replypost(user.username)
            pid = newreply.rpid
            return render_template('tmppage.html', picture=1, v=url_for('bbs.postdetail', pid=post.pid),
                                   i='回复成功！获得10金币和2积分', **locals())
        return render_template('login.html', **locals())
    else:
        post.phits += 1
        post.save_one()
        return render_template('postdetail.html', **locals())


# 发帖子
@bbs.route('/edit/<int:cid>', methods=['GET', 'POST'])
def editpost(cid=0):
    if session.get('username'):
        categories = Category.query.filter(Category.cpid == 0).all()
        smallc = Category.query.filter(Category.cid == cid).first()
        bigc = Category.query.filter(Category.cid == smallc.cpid).first()
        posts = Posts.query.filter(Posts.pcid == cid).all()
        if request.method == 'POST':
            print(request.args.get(cid))
            user = User.query.filter(User.username == session['username']).first()
            title = request.form.get('subject')
            content = request.form.get('mycontent')
            postuser = user.username
            # 生成一条帖子记录
            newpost = Posts(ptitle=title, pcontent=content, puser=postuser, pcid=cid)
            newpost.save_one()
            pid = newpost.pid
            # 更新user信息
            user.editpost()
            user.setsession()
            # 更新板块信息
            smallc.editpost(user.username)
            return render_template('tmppage.html', picture=1, v=url_for('bbs.postdetail', pid=pid), i='发帖成功！获得50金币和5积分',
                                   **locals())
        return render_template('editpost.html', **locals())
    return render_template('login.html', **locals())


# 设置当前时间
@bbs.route('/moment/')
def custom_time():
    current = datetime.utcnow()
    return render_template('common/Base.html', time=current)

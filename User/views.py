from flask import Blueprint, render_template, request, redirect, make_response, url_for, session
from User.models import *

# 实例化bbs
bbs = Blueprint('bbs', __name__, url_prefix='')


# 首页
@bbs.route('/index/')
@bbs.route('/index/<int:cid>')
def index(cid=0):
    categories, smallcategory, bigc, smallc = Category.show_category(cid)
    posts = Posts.query.filter(Category.cid == cid).all()
    postscount = db.session.query(Posts).count()
    userscount = db.session.query(User).count()
    newuser = User.query.order_by(User.uid).all()
    return render_template('index.html', title='首页', **locals())


# 帖子列表
@bbs.route('/posts/')
@bbs.route('/posts/<int:cid>')
@bbs.route('/posts/<int:cid>/<int:elite>')
def posts(cid=0, elite=0):
    categories, smallcategory, bigc, smallc = Category.show_category(cid)
    if elite == 1:
        posts = Posts.query.filter(Posts.pcid == cid, Posts.piselite == 1, Posts.pisdel == 0).all()
    else:
        posts = Posts.query.filter(Posts.pcid == cid, Posts.pisdel == 0, ).order_by(-Posts.pistop, -Posts.piselite,
                                                                                    -Posts.pislight, -Posts.preplycount,
                                                                                    Posts.plastreplytime).all()
    replies = Replies.query.all()
    return render_template('postlist.html', title='post', **locals())


# 帖子详细信息、回帖
@bbs.route('/detail/<int:pid>')
@bbs.route('/detail/<int:pid>', methods=['GET', 'POST'])
def postdetail(pid=1):
    session['pid'] = pid
    cid = Posts.query.filter(Posts.pid == pid).first().pcid
    posts = Posts.query.filter(Posts.pcid == cid).all()
    categories, smallcategory, bigc, smallc = Category.show_category(cid)
    post = Posts.query.filter(Posts.pid == pid).first()
    replies = Replies.query.filter(Replies.rpid == pid).all()
    replylist = []
    replyfloor = 0
    for reply in replies:
        replyfloor += 1
        replyuser = User.query.filter(User.username == reply.replyuser).first()
        replylist.append([reply, replyuser, replyfloor])
    postuser = User.query.filter(User.username == post.postuser).first()
    lastreplyuser = User.query.filter(User.username == post.plastreplyuser).first()
    if request.method == 'POST':
        if session.get('username'):
            user = User.query.filter(User.username == session['username']).first()
            myreply = request.form.get('myreply')
            newreply = Replies(rcontent=myreply, replyuser=user.username, rpid=post.pid)
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
                                   i='回复成功！获得2金币和1积分', **locals())
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
            newpost = Posts(ptitle=title, pcontent=content, postuser=postuser, pcid=cid)
            newpost.save_one()
            pid = newpost.pid
            session['pid'] = pid
            # 更新user信息
            user.editpost()
            user.setsession()
            # 更新板块信息
            smallc.editpost(newpost.ptitle)
            return render_template('tmppage.html', picture=1, v=url_for('bbs.postdetail', pid=pid), i='发帖成功！获得5金币和2积分',
                                   **locals())
        return render_template('editpost.html', **locals())
    return render_template('login.html', **locals())


# 设置当前时间
@bbs.route('/moment/')
def custom_time():
    current = datetime.utcnow()
    return render_template('common/Base.html', time=current)


# 帖子高亮
@bbs.route('/postlight/<int:pid>/<int:light>', methods=['GET', 'POST'])
def post_light(pid=0, light=0):
    post = Posts.query.filter(Posts.pid == pid).first()
    post.pislight = light
    post.save_one()
    pid = post.pid
    return redirect(url_for('bbs.postdetail', **locals()))


# 帖子置顶
@bbs.route('/posttop/<int:pid>/<int:top>', methods=['GET', 'POST'])
def post_top(pid=0, top=0):
    post = Posts.query.filter(Posts.pid == pid).first()
    post.pistop = top
    post.save_one()
    pid = post.pid
    return redirect(url_for('bbs.postdetail', **locals()))


# 帖子删除
@bbs.route('/postdel/<int:pid>/<int:delete>', methods=['GET', 'POST'])
def post_del(pid=0, delete=0):
    post = Posts.query.filter(Posts.pid == pid).first()
    post.pisdel = delete
    post.save_one()
    pid = post.pid
    return redirect(url_for('bbs.postdetail', **locals()))


# 帖子加精
@bbs.route('/postelite/<int:pid>/<int:elite>', methods=['GET', 'POST'])
def post_elite(pid=0, elite=0):
    post = Posts.query.filter(Posts.pid == pid).first()
    post.piselite = elite
    post.save_one()
    pid = post.pid
    return redirect(url_for('bbs.postdetail', **locals()))

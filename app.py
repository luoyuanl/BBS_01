from flask import Flask, redirect
from flask_login import login_manager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import configure_uploads, patch_request_class

from User.check_login import us
from User.views import bbs
from ext import db, moment, photos

app = Flask(__name__)
app.config.from_pyfile('settings.py')

manager = Manager(app)

# 注册蓝图
app.register_blueprint(bbs)
app.register_blueprint(us)

# 初始化对象
db.init_app(app)
moment.init_app(app)

# 数据库迁移
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

# 配置文件上传对象
configure_uploads(app, photos)
# 若设置为None,则以MAX_CONTENT_LENGTH配置为准
patch_request_class(app, size=None)


@app.route('/')
def hello_world():
    return redirect('/index/')


if __name__ == '__main__':
    manager.run()

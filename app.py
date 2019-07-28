from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from User.views import bbs
from ext import db

app = Flask(__name__)
app.config.from_pyfile('settings.py')

manager = Manager(app)

# 注册蓝图
app.register_blueprint(bbs)

# 初始化数据库对象
db.init_app(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

@app.route('/')
def hello_world():
    return 'hello world'


if __name__ == '__main__':
    manager.run()

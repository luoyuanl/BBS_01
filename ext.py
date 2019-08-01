# 所有的扩展
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES

# 实例化一个数据库对象
db = SQLAlchemy()
# 实例化一个moment对象
moment = Moment()
# 实例化文件上传对象
photos = UploadSet('photos', IMAGES)
# 发邮件
mail = Mail()
# 实例化一个验证登录对象
login_manager = LoginManager()

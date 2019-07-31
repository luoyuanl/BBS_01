# 数据库配置
import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:524107@10.0.108.41/bbs_data'


# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:524107@192.168.249.201:3306/bbs_data'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = 'DSAG3842AS'

CACHE_TPYE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 1

# 邮件
MAIL_SERVER = 'smtp.qq.com'
MAIL_USERNAME = '521149380@qq.com'
MAIL_PASSWORD = '授权码'
# MAIL_PORT


# file-uploads文件上传设置
UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'static/upload')
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 图片大小

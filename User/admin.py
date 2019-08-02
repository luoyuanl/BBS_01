from flask import Blueprint

# 实例化user
admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('//')
def post_top():
    pass

@admin.route('//')
def post_ligth():
    pass

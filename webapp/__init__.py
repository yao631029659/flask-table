from flask import Flask,redirect,url_for
from webapp.extensions import bcrypt,login_manager
# 引入认证文件
from webapp.config import DevConfig
# 引入db db=Sqlalchemy（app）
from webapp.models import db
# 这个是为了认证蓝图
from webapp.controllers.blog import blog_blueprint
from webapp.controllers.main import main_blueprint
# from webapp.extensions import oath
from webapp.extensions import oid,principals
from flask_principal import identity_loaded,UserNeed,RoleNeed
from flask_login import current_user
# 这里一共有三句重要的代码


def create_app(object_name):
    '''博客程序'''
    app = Flask(__name__)
    # 从app下的config导入配置
    app.config.from_object(object_name)
    # SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
    # 相当于 db=Sqlalchemy（app）
    db.init_app(app) #第一
    # FlaskBcrypt与Flask SQLAlchemy 一样需要使用app对象来进行初始化
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    # 只要一登陆 就用current_user的id值生成UserNeed类
    # 只要一登陆 就用current_user的role生成RoleNeed类
    #identity.provides 给userneed类添加roleneed角色
    # 现在每当当前用户（身份）发生变化的时候，都会添加一个UserNeed来记录这个用户，通过RoleNeed来记录它的权限
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender,identity):
        print("传递过来的identity的值是", identity)
        # 和flask_login的关系在此建立
        identity.user = current_user
        print("identity的值是", identity)
        if hasattr(current_user,'id'):
            # 新增Need(method='id', value=1)
            identity.provides.add(UserNeed(current_user.id))
            print("identity的值是", identity)
        if hasattr(current_user,'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
            print("identity的值是", identity)

    @app.route('/')
    def index():
        # 不能写.home哦 #第二跳转到url_for
        return redirect(url_for('blog.home'))
    # 注册蓝图 第三
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main_blueprint)
    return app



if __name__=='__main__':
    app=create_app('webapp.config.DevConfig')
    app.run()


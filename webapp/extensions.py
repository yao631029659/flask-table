from flask_bcrypt import Bcrypt
from flask_openid import OpenID
# from flask_oauth import OAuth
from flask_login import LoginManager

bcrypt=Bcrypt()
oid = OpenID()
# oath = OAuth()
login_manager=LoginManager()
# 哪一个视图作为登陆页面 下面这些是默认配置 如果觉得不好用可以直接用 @login_manager.unauthorized_handler() 来写
# 默认登陆的视图 main是蓝图名字 login是main下面的控制器
login_manager.login_view = 'main.login'
# 保护等级
login_manager.session_protection='strong'
# 默认的提示登陆的信息
login_manager.login_message = '请登录'
login_manager.login_message_category = 'info'

# 让底层可以userid回调高层的load_user 并读取对应的User到底层去
@login_manager.user_loader
def load_user(userid):
    from webapp.models import User
    # 注意返回值 是User
    return User.query.get(userid)

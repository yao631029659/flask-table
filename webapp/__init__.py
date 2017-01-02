from flask import Flask,redirect,url_for
from webapp.extensions import bcrypt
# 引入认证文件
from webapp.config import DevConfig
# 引入db db=Sqlalchemy（app）
from webapp.models import db
# 这个是为了认证蓝图
from webapp.controllers.blog import blog_blueprint
# 这里一共有三句重要的代码
app = Flask(__name__)
# 从app下的config导入配置
app.config.from_object(DevConfig)
# SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
# 相当于 db=Sqlalchemy（app）
db.init_app(app) #第一
# FlaskBcrypt与Flask SQLAlchemy 一样需要使用app对象来进行初始化
bcrypt.init_app(app)
@app.route('/')
def index():
    # 不能写.home哦 #第二跳转到url_for
    return redirect(url_for('blog.home'))
# 注册蓝图 第三
app.register_blueprint(blog_blueprint)
if __name__ == '__main__':
    app.run()

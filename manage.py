import os
from flask_script import Manager, Server
# 现在app被拆到第一行了 原来在第二行的
from webapp import create_app
from webapp.models import db,User,Post,Comment,Tag,tags,Role

# 初始化app
# 都会获取一次 OS 的环境变量，并以此来创建 app 对象 os.environ可以读取到所有的环境变量 而且是以字典存在的
#下面这个的意思是 读取环境变量里面WEBAPP_ENV的值 如果没有 那就用dev这个默认值
env = os.environ.get('WEBAPP_ENV','dev')
# 如果上面一句用了默认值 那么下面这句就会变成'webapp.config.DevConfig'
app = create_app('webapp.config.%sConfig'% env.capitalize())
# 用manager管理app
manager = Manager(app)
# 导入到命令行
manager.add_command("server", Server())

@manager.shell #写下面函数的好处就是再shell命令行调用的时候不用写 from main import db 了
def make_shell_context():
    return dict(app=app,db=db,User=User,Post=Post,Comment=Comment,Tag=Tag,tags=tags,Role=Role)

if __name__ == "__main__":
    manager.run()

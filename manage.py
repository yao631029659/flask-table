from flask_script import Manager, Server
# 现在app被拆到第一行了 原来在第二行的
from webapp import app
from webapp.models import db,User,Post,Comment,Tag,tags

# 用manager管理app
manager = Manager(app)
# 导入到命令行
manager.add_command("server", Server())

@manager.shell #写下面函数的好处就是再shell命令行调用的时候不用写 from main import db 了
def make_shell_context():
    return dict(app=app,db=db,User=User,Post=Post,Comment=Comment,Tag=Tag,tags=tags)

if __name__ == "__main__":
    manager.run()

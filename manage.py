from flask_script import Manager, Server
#修正中文乱码了
# 这里引用main.py 就在当前路径下
from main import app,db,User
# 用manager管理app
manager = Manager(app)
# 导入到命令行
manager.add_command("server", Server())

@manager.shell #写下面函数的好处就是再shell命令行调用的时候不用写 from main import db 了
def make_shell_context():
    return dict(app=app,db=db,User=User)

if __name__ == "__main__":
    manager.run()

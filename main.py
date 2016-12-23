#一个生成app实例
#第二生成数据库 修正中文乱码了
from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 从app下的config导入配置
app.config.from_object(DevConfig)
# 传递给数据库
db=SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255))
    password=db.Column(db.String(255))
    # lazy = subquery: 会在加载Post对象后，将与Post相关联的对象全部加载，这样就可以减少Query的动作，也就是减少了对DB的I / O操作。但可能会返回大量不被使用的数据，会影响效率。
    # lazy = dynamic: 只有被使用时，对象才会被加载，并且返回式会进行过滤，如果现在或将来需要返回的数据量很大，建议使用这种方式。
    posts=db.relationship('Post',backref='user',lazy='subquery')
    def __init__(self,username):
        self.username=username

    # 刚开始的时候 没写这句结果一用 users的时候老是报main 0x错误 搞了我一整天 我还以为是中文编码的问题呢 原来是错在这里
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(255))
    text=db.Column(db.Text())
    push_date=db.Column(db.DateTime())
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __init__(self,title):
        self.title=title

    def __repr__(self):
        return '<Post {}>'.format(self.title)




@app.route('/')
def home():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run()

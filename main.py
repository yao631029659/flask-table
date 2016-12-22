#一个生成app实例
#第二生成数据库
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

@app.route('/')
def home():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run()

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from sqlalchemy import func
# 生成app
app=Flask(__name__)
# 引用config文件
app.config.from_object(DevConfig)
# 实例化sqlalchemy
db=SQLAlchemy(app)
tags_table=db.Table(
    'post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)
# 生成用户表 用户表和post表是一对多的关系
class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts=db.relationship('Post',backref='user',lazy='dynamic')
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return '<User %s>'%self.name
# 生成post表 post表和comment表是一对多关系
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(255))
    text=db.Column(db.Text())
    publish_date=db.Column(db.DateTime())
    comments=db.relationship('Comment',backref='post',lazy='dynamic')
    user_id=db.Column(db.Integer(),db.ForeignKey(User.id))
    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return '<Post %s>'%self.title


    tags=db.relationship('Tag',secondary='post_tags',backref=db.backref('posts',lazy='dynamic'))
# 生成comment表
class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(255))
    text=db.Column(db.Text())
    date=db.Column(db.DateTime())
    post_id=db.Column(db.Integer(),db.ForeignKey(Post.id))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Comment %s>'%self.name


# 生成tag表 tag表和post表是多对多的关系
class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return '<Tag %s>'%self.title
def side_data():
    # 单表查询可以直接用这一个
    rencent=Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    # 多表查询用下面这种格式 用db开头的
    top_tag=db.session.query(Tag,db.func.count(tags_table.c.post_id).label('total')).join(tags_table).group_by(Tag).order_by('total DESC').limit(5).all()
    return rencent,top_tag
# 写路由规则
# home控制器
@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts=Post.query.order_by(Post.publish_date.desc()).paginate(page,10)
    recent,top_tag=side_data()
    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tag=top_tag
    )
# post控制器
# By default, a route only answers to GET requests, but that can be changed by providing the methods argument to the route() decorator.
@app.route('/post/<int:post_id>',methods=('GET','POST'))
def post():
    recent, top_tag = side_data()



# tag控制器
@app.route('/tag/<string:tag_name>')
def tag():
    recent, top_tag = side_data()

# user控制器
app.route('/user/<string:username>')
def username():
    recent, top_tag = side_data()
# run app
if __name__=="__main__":
    app.run()
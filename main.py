from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
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
    posts=db.relationship('Post',backref='user',lazy='subquery')
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
    comments=db.relationship('Comment',backref='post',lazy='subquery')
    user_id=db.Column(db.Integer(),db.ForeignKey(User.id))
    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return '<Post %s>'%self.title


    tags=db.relationship('Tag',secondary='post_tags',backref=db.backref('posts',lazy='subquery'))
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
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Tag %s>'%self.name

# run app
if __name__=="__main__":
    app.run()
from flask_sqlalchemy import SQLAlchemy
from webapp.extensions import bcrypt
from flask_login import AnonymousUserMixin,UserMixin
db=SQLAlchemy()
# model不用应用其它数据
# 多对多表关系 不过需要去init里面实例化一下 用的方法是db.init_app(app) 相当于之前的db=SQLchemy（app）这样db.model才能用
tags=db.Table(
    'post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255))
    password=db.Column(db.String(255))
    # lazy = subquery: 会在加载Post对象后，将与Post相关联的对象全部加载，这样就可以减少Query的动作，也就是减少了对DB的I / O操作。但可能会返回大量不被使用的数据，会影响效率。
    # lazy = dynamic: 只有被使用时，对象才会被加载，并且返回式会进行过滤，如果现在或将来需要返回的数据量很大，建议使用这种方式。
    #backref 允许我们从多端向当前一端进行修改Post.user
    posts=db.relationship('Post',backref='user',lazy='subquery')
    def __init__(self,username,password):
        self.username=username
        # 调用自身的函数来生成哈希值 结果直接保存到password里面
        self.password=self.set_password(password)

    # 刚开始的时候 没写这句结果一用 users的时候老是报main 0x错误 搞了我一整天 我还以为是中文编码的问题呢 原来是错在这里
    def __repr__(self):
        return '<User {}>'.format(self.username)
    # 67页 新增部分 在模型里面定义的函数一般和数据库查询有关系 比如在数据库里面是不是存在这种

    def set_password(self,password):
        self.password=bcrypt.generate_password_hash(password)
        return bcrypt.generate_password_hash(password)

    def check_password(self, password): #self.password 是密码的哈希值 前面没有点的真实的密码值
        return bcrypt.check_password_hash(self.password, password)

    # 检验User的实例化对象是否登录了.
    # def is_authenticcated(self):
    #     if isinstance(self,AnonymousUserMixin):
    #         return False
    #     else:
    #         return True
    #
    # # 检验用户是否通过某些验证
    # def is_active(self):
    #     return True
    #
    # # 检验用户是否为匿名用户
    # def is_anoymous(self):
    #     if isinstance(self, AnonymousUserMixin):
    #         return True
    #     else:
    #         return False
    #
    # # 返回User实例化对象的唯一标识id
    # def get_id(self):
    #     return unicode(self.id)

class Post(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(255))
    text=db.Column(db.Text())
    publish_date=db.Column(db.DateTime())
    writer = db.Column(db.String(255))
    # 不建议使用User.id(对象属性) user.id是类属性相当于 __tablename__

    comments=db.relationship(
        # 子表名字
        'Comment',
        #父表名字
        backref='post',
        lazy='dynamic'
    )
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # many to many: posts <==> tags
    tags = db.relationship(
        # 和post关联的表是Tag(tag)
        'Tag',
        # 关系保存在tags里面 db.table的那个
        secondary=tags,
        # db.backref 这个关系字段焦作posts
        backref=db.backref('posts',lazy='dynamic')
    )

    def __init__(self,title):
        self.title=title

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Comment(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(255))
    text=db.Column(db.Text())
    date=db.Column(db.DateTime())
    post_id=db.Column(db.Integer(),db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

class Tag(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(255))

    def __init__(self,title):
        self.title=title
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)
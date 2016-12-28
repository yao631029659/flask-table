import datetime

from flask import Flask,render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,or_
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
# 从app下的config导入配置
app.config.from_object(DevConfig)
# SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
db=SQLAlchemy(app)
# 多对多表关系
tags=db.Table(
    'post_tags',
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255))
    password=db.Column(db.String(255))
    # lazy = subquery: 会在加载Post对象后，将与Post相关联的对象全部加载，这样就可以减少Query的动作，也就是减少了对DB的I / O操作。但可能会返回大量不被使用的数据，会影响效率。
    # lazy = dynamic: 只有被使用时，对象才会被加载，并且返回式会进行过滤，如果现在或将来需要返回的数据量很大，建议使用这种方式。
    #backref 允许我们从多端向当前一端进行修改Post.user
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
    publish_date=db.Column(db.DateTime())
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
# 表单第一步 继承form类
class CommentForm(Form):
    name = StringField(
        # 这个在列表里面叫 form.name.label
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

# 方便多次引用 home就引用了 返回的是rencent 和top_tag
def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    # top_tags里面一共有三列
    top_tags=db.session.query(
        # Tag(tag)就是那个表关系模型表 # tags(post_tags) 是那个关系表 # label把列名改成total # post.c  c的意思是column的意思
        Tag,func.count(tags.c.post_id).label('total')
        # .join让关系表tags和Tag连接在一起
    ).join(
        tags
    # group_by(Tag) 就是 GROUP BY tag.id, tag.title #  order by total DESC  total是列名哦
    ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent,top_tags



@app.route('/')
# 把接收回来的函数 转换成int 赋值给page
@app.route('/<int:page>')
def home(page=1):
    # 第一次使用的使用要从类(Post)里面query posts已经是pagination对象了 这个对象有 has_next :是否还有下一页 has_prev :是否还有上一页 这些方法
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template(
        'home.html',
        # 传递值给模板
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
@app.route('/post/<int:post_id>',methods=('GET','POST'))
def post(post_id):
    # 创建表单对象实例
    form = CommentForm()
    # 如果使用了post方法 点击提交view页面的提交 才会执行 看到没有数据传回来了
    if form.validate_on_submit():
        # 这个comment就是我们定义的表 class Commnent() 磨刀霍霍向猪羊 数据都准备好了 要提交了
        # 还记得 user=User.query.all()吗？
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        # post_id是路由传过来的数据
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()

        db.session.add(new_comment)
        db.session.commit()

    # 如果没有找到返回404错误 没有找到需要评论的文章
    post=Post.query.get_or_404(post_id)
    tags=post.tags
    comments=post.comments.order_by(Comment.date.desc()).all()
    recent,top_tags=sidebar_data()
    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        # 表单发出去了 上面回收哦
        form=form
    )
@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag=Tag.query.filter_by(title=tag_name).first_or_404()
    posts=tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'tag.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
@app.route('/user/<string:username>')
def user(username):
    # .如果在view function中不想让后台报None错误的话，可以通过get_or_404() 取代get() 方法、first_or_404() 取代first()方法，使得前台报404错误。
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=user,
        posts=post,
        recent=recent,
        top_tags=top_tags
    )
if __name__ == '__main__':
    app.run()

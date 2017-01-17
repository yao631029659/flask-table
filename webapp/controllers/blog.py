import datetime
from flask import Blueprint,render_template,url_for,redirect
from flask_login import login_required,current_user
# 新的架构把表单和模型从控制器里面分离出去了 所以在这里要引入回来
# 这个文件就相当于之前的main文件 main文件一直在运行 现在你把它写到里面来了 在原来的文件里面写蓝图 让它也运行里面的东西
# 蓝图又和数据库打交道又和表现层打交道 所以两个文件都要引入
from webapp.models import db,Post,Tag,Comment,User,tags
from webapp.forms import CommentForm,PostForm
from sqlalchemy import func
from webapp.extensions import poster_permission

blog_blueprint = Blueprint(
    'blog',
    __name__,
    # 比第四章加了../
    template_folder='../templates/blog',
    url_prefix="/blog"
)

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



# 把接收回来的函数 转换成int 赋值给page
@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    # 第一次使用的使用要从类(Post)里面query posts已经是pagination对象了 这个对象有 has_next :是否还有下一页 has_prev :是否还有上一页 这些方法
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    recent,top_tags = sidebar_data()
    return render_template(
        'home.html',
        # 传递值给模板
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
@blog_blueprint.route('/post/<int:post_id>',methods=('GET','POST'))
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
@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag=Tag.query.filter_by(title=tag_name).first_or_404()
    posts=tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags,
    )
@blog_blueprint.route('/user/<string:username>')
def user(username):
    # .如果在view function中不想让后台报None错误的话，可以通过get_or_404() 取代get() 方法、first_or_404() 取代first()方法，使得前台报404错误。
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )

@blog_blueprint.route('/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post =Post(form.title.data)
        new_post.text=form.text.data
        new_post.publish_date=datetime.datetime.now()
        new_post.writer = current_user.username
        # new_post.user = User.query.filter_by(username=current_user.username)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('.home'))
    return render_template('new.html',form=form)

@blog_blueprint.route('/edit/<int:id>',methods=['GET','POST'])
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)
    form=PostForm()
    print('edit_post被调用')
    if form.validate_on_submit():
        print('edit_post事务')
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()
        db.session.add(post)
        db.session.commit()
        print('edit_post事务')
        return redirect(url_for('.post',post_id=post.id))
    form.text.data = post.text
    form.title.data = post.title
    return render_template('edit.html',form=form,post=post)



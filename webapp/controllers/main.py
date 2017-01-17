from flask import Blueprint,redirect,url_for,flash,render_template
from webapp.forms import LoginForm,RegisterForm
from webapp.models import User,db
from flask_login import login_user,logout_user,login_required
from flask_principal import Identity,AnonymousIdentity,identity_changed,current_app

main_blueprint=Blueprint(
    'main',
    __name__,
    template_folder='../templates/main',
)
@main_blueprint.route('/',methods=['get','post'])
def index():
    return redirect(url_for('blog.home'))

# 登陆的视图函数
@main_blueprint.route('/login',methods=['get','post'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(
            username=form.username.data
        ).one()
        # 好了 用了这句flask—login就起作用了
        print('点击了记住我')
        print(form.remember.data)
        login_user(user, remember=form.remember.data)
        # 发送信号给 @identity_loaded.connect_via(app) 修饰的函数
        identity_changed.send(
            # 当前app
            current_app._get_current_object(),
            # 当前的用户id 我觉得这里有点多余 因为在__init__.py 里面不是读取了current_user吗？
            identity=Identity(user.id)
        )

        flash('you have logged in',category='success')
        return redirect(url_for('blog.home'))

    return render_template(
        'login.html',
        form=form
    )

# 退出
@main_blueprint.route('/logout',methods=['get','post'])
@login_required
def logout():
    flash('you have logged out',category='success')
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        # 一旦退出改变身份成为匿名身份
        identity=AnonymousIdentity()
    )
    return redirect(url_for('blog.home'))

#注册
@main_blueprint.route('/register',methods=['get','post'])
def register():
    form=RegisterForm()
    # 通过检查了就会跑到if里面去了
    if form.validate_on_submit():
        new_user = User(form.username.data,form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('your user has been created,please login.',category='success')
        # 同一级的可以用.login跳转
        return redirect(url_for('.login'))
    # 如果没有通过检查
    return render_template(
        'register.html',
        form=form
    )


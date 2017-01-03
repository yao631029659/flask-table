from flask import Blueprint,redirect,url_for,flash,render_template
from webapp.forms import LoginForm,RegisterForm
from webapp.models import User,db
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
        flash('you have logged in',category='success')
        return '登陆成功'
    else:
        flash('登陆失败',category='warning')

    return render_template(
        'login.html',
        form=form
    )

# 退出
@main_blueprint.route('/logout',methods=['get','post'])
def logout():
    flash('you have logged out',category='success')
    return redirect(url_for('.home'))

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
        return redirect(url_for('.login'))
    # 如果没有通过检查
    return render_template(
        'register.html',
        form=form
    )
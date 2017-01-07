from wtforms import StringField, TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,URL
from flask_wtf import Form,RecaptchaField
from webapp.models import User
# 专门写wtf类
# 表单第一步 继承form类
class CommentForm(Form):
    name = StringField(
        # 这个在列表里面叫 form.name.label
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

# 登陆表单
class LoginForm(Form):
    username=StringField('username',
    [DataRequired(),Length(max=255)]
    )
    password=PasswordField('password',
    [DataRequired()])

    # 验证函数
    def validate(self):
        # 验证方法继承了 上一个继承的super的validate方法 然后又添加了新的方法进来 还用原来的函数名 super用来解决多重继承的问题 就算Form改名这里也不用改
        check_validate=super().validate()
    # 如果验证没有通过的话 这个是哪个super类的原始方法
        if not check_validate:
            print('基本验证都通过不了')
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append(
                '没有找到用户名'
            )
            print('没有找到用户名')
            return False

        # 运行到这里都没有return的话 那至少有用户名了
        # 这个check_password是在model里面写的 在这里用了

        if not user.check_password(self.password.data):
            self.password.errors.append(
                '密码不正确'
            )
            print('密码不正确')
            return False
        return True

class RegisterForm(Form):
    username=StringField('username',[DataRequired(),Length(max=255)])
    password=PasswordField('password',[DataRequired(),Length(min=8)])
    # 重复一次
    confirm=PasswordField('confirm',[DataRequired(),EqualTo('password')])
    # 谷歌验证码 谁能告诉我为什么不用recaptcha.init(app)啊
    # recaptcha=RecaptchaField()  在中国你懂的
    def validate(self):
        check_validate=super().validate()
        if not check_validate:
            print('基本验证不通过')
            return False
        user=User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(
                '用户名已经存在'
            )
            print('用户名已经存在')
            return False
        return True
class PostForm(Form):
    title=StringField('Title',[DataRequired(),Length(max=255)])
    text = TextAreaField('Content',[DataRequired()])
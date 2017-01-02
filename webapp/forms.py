from wtforms import StringField, TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,URL
from flask_wtf import Form
# 专门写wtf类
# 表单第一步 继承form类
class CommentForm(Form):
    name = StringField(
        # 这个在列表里面叫 form.name.label
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])
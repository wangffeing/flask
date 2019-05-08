from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import Regexp, ValidationError, EqualTo, InputRequired

class SigninForm(BaseForm):
    zxbh = StringField(validators=[Regexp(r'[0-9]{8,8}', message='请输入正确的在线编号')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,15}', message='请输入正确格式的密码')])
    remember = StringField()

class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = IntegerField(validators=[InputRequired(message='请选择版块')])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])
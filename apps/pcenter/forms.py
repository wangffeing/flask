from wtforms import StringField,IntegerField, FileField
from wtforms.validators import InputRequired,Length,EqualTo
from ..forms import BaseForm


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(1, 20, message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(1, 20, message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='兩次输入的密码不一致')])


class AddBoardsForm(BaseForm):
    name=StringField(validators=[InputRequired(message='请输入版块名称'),Length(2,15,message='长度应在2-15个字符之间')])


class UpdateBoardForm(AddBoardsForm):
    board_id=IntegerField(validators=[InputRequired(message='请输入版块名称')])


class EditProfileForm(BaseForm):
    name = StringField(validators=[Length(0, 64, message='请输入姓名')])
    avatar = FileField('头像')
import shortuuid
import enum
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.functions import concat

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    zxbh = db.Column(db.String(50),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100), default='image/avatar/default.png')
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self, *args, **kwargs):
        # 如果传入的参数里面有‘password’，就单独处理
        if "password" in kwargs:
            self.password = kwargs.get("password")
            # 处理完后把password pop出去
            kwargs.pop("password")
            # 剩下的参数交给父类去处理
        super(User, self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    # 保存密码的时候加密
    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):
        # 用户拥有的权限
        if not self.roles:
            return 0
        all_permissions = 0
        # 用户所有的角色
        for role in self.roles:
            # 取出用户所有角色的所有权限
            permissions = role.permissions
            # 把所有权限通过“|=”整合到all_permissions
            all_permissions |= permissions

        return all_permissions

    def has_permission(self, permission):
        # 判断用户是否有'xxx'权限
        # 通过与操作判断用户是否有权限，结果相同返回true，不相等返回false
        return self.permissions & permission == permission

    @property
    def is_developer(self):
        return self.has_permission(Permission.ALL_PERMISSION)

    def is_voted(self, post_id):
        for post in self.postvote:
            if post.post_id == post_id:
                return True
        return False

class Permission(object):
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR = 0b00000001
    # 2. 管理帖子、评论权限
    POSTER = 0b00000010
    # 3. 管理用户的权限
    USER = 0b00000100
    # 4. 管理板块的权限
    BOARDER = 0b00001000
    # # 5. 待定
    # FRONTUSER = 0b00010000
    # # 6. 待定
    # CMSUSER = 0b00100000
    # # 7. 待定
    # ADMINER = 0b01000000

role_user = db.Table(
    'role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('user_id', db.String(100), db.ForeignKey('user.id'), primary_key=True)
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=Permission.VISITOR)
    users = db.relationship('User', secondary=role_user, backref='roles')


class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    read_count = db.Column(db.Integer, default=0)
    board = db.relationship('BoardModel', backref='posts')
    author_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)

    author = db.relationship('User', backref='posts')

    @hybrid_property
    def title_content(self):
        return '{0} {1}'.format(self.title.encode('utf-8'),
                                self.content.encode('utf-8'))

    @title_content.expression
    def title_content(cls):
        # return literal_column('title || " " || content')
        return concat(cls.title, cls.content)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)

    post = db.relationship("PostModel",backref='comments')
    author = db.relationship("User",backref='comments')


class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    create_time = db.Column(db.DateTime,default=datetime.now)

    post = db.relationship("PostModel",backref="highlight")

class VotePostUserModel(db.Model):
    __tablename__ = 'votepost_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))

    postv = db.relationship("PostModel", backref="vote")
    userv = db.relationship("User", backref="postvote")
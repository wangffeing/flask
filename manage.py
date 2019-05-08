from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from exts import db
import config
from apps.models import User, Role, Permission, BannerModel, BoardModel, PostModel

app = create_app()
manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-z', '--zxbh', dest='zxbh')
def create_user(username, password, zxbh):
    user = User(username=username, password=password, zxbh=zxbh)
    db.session.add(user)
    db.session.commit()
    print('用户添加成功')

@manager.command
def create_role():
    # 1. 访问者（可以修改个人信息）
    visitor = Role(name='访问者', desc='只能访问数据，不能修改')
    visitor.permissions = Permission.VISITOR

    # 2.运营人员（修改个人信息，管理帖子，管理评论）
    operator = Role(name='运营', desc='管理帖子，管理评论')
    operator.permissions = Permission.VISITOR | Permission.POSTER

    # 3.管理员（拥有所有权限）
    admin = Role(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = Permission.VISITOR | Permission.POSTER | Permission.USER | Permission.BOARDER

    # 4.开发者
    developer = Role(name='开发者', desc='开发人员专用角色')
    developer.permissions = Permission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()

@manager.command
def create_test_post():
    for x in range(100):
        title = '我是标题%s'%x
        content = '我是内容，我的编号是%s'%x
        board = BoardModel.query.first()
        author = User.query.first()
        post = PostModel(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('测试帖添加成功')

@manager.option('-z', '--zxbh',  dest='zxbh') #用户在线编号
@manager.option('-n', '--name',  dest='name') #角色名字
def add_user_to_role(zxbh, name):
    # 添加用户到某个角色
    user = User.query.filter_by(zxbh=zxbh).first()
    if user:
        role = Role.query.filter_by(name=name).first()
        if role:
            # 把用户添加到角色里
            role.users.append(user)
            db.session.commit()
            print("用户成功添加到角色")
        else:
            print("没有这个角色：%s" % role)
    else:
        print("%s 没有这个编号" % zxbh)


@manager.command
def test_permission():
    # 测试用户是否有xxx权限
    user = User.query.first()
    if user.has_permission(Permission.VISITOR):
        print("这个用户有访问者权限")
    else:
        print("这个用户没有访问者权限")


if __name__ == '__main__':
    manager.run()
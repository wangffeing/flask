from flask import Blueprint, views, render_template, request, session, g
from ..decorators import login_required, permission_required
from .forms import ResetpwdForm, AddBoardsForm, UpdateBoardForm
from ..models import User, Permission, Role, BannerModel, BoardModel, HighlightPostModel, PostModel, CommentModel
from exts import db
from utils import restful
from flask_paginate import Pagination, get_page_parameter
import config
import os

bp = Blueprint("pcenter",__name__,url_prefix='/pcenter/')

@bp.route('/')
@login_required
def index():
    return render_template('pcenter/pc_index.html')

@bp.route('/profile/')
@login_required
def profile():
    return render_template('pcenter/pc_profile.html')

@bp.route('/avatar/', methods=['GET', 'POST'])
@login_required
def avatar():
    if request.method == 'POST':
        file = request.files['avatar_upload']
        base_path = config.UPLOADED_AVATER_PATH
        filename = str(g.user.id) + '.' + file.filename.rsplit('.', 1)[1]
        file_path = os.path.join(base_path, filename)
        file.save(file_path)
        g.user.avatar = 'image/avatar/' + filename
        db.session.commit()

        return restful.success()
    else:
        return render_template('pcenter/pc_resetavatar.html')

@bp.route('/boards/')
@login_required
@permission_required(Permission.BOARDER)
def boards():
    board_models=BoardModel.query.all()
    context={
        'boards':board_models
    }
    return render_template('pcenter/pc_boards.html',**context)

@bp.route('/aboards/',methods=['POST'])
@login_required
@permission_required(Permission.BOARDER)
def aboards():
    form=AddBoardsForm(request.form)
    if form.validate():
        name=form.name.data
        board=BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboards/',methods=['POST'])
@login_required
@permission_required(Permission.BOARDER)
def uboards():
    form=UpdateBoardForm(request.form)
    if form.validate():
        board_id=form.board_id.data
        name=form.name.data
        board=BoardModel.query.get(board_id)
        if board:
            board.name=name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个版块')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboards/',methods=['POST'])
@login_required
@permission_required(Permission.BOARDER)
def dboards():
    board_id=request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='请传入版块ID')
    board=BoardModel.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='没有这个版块')


@bp.route('/posts/')
@login_required
@permission_required(Permission.POSTER)
def posts():

    # post_list = PostModel.query.all()
    # return render_template('cms/cms_posts.html', posts=post_list)

    # 获取当前页码数
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.MANAGE_PER_PAGE
    end = start + config.MANAGE_PER_PAGE

    query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, per_page=config.MANAGE_PER_PAGE)
    posts = query_obj.slice(start, end)

    context = {
        'posts': posts,
        'pagination': pagination,
    }
    return render_template('pcenter/pc_posts.html', **context)


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(Permission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id!')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(Permission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/dposts/',methods=['POST'])
@login_required
@permission_required(Permission.POSTER)
def dposts():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id!')
    post = PostModel.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return restful.success(message='deleted!')
    else:
        return restful.params_error(message='没有这篇帖子')


@bp.route('/comments/')
@login_required
@permission_required(Permission.POSTER)
def comments():
    # post_list = PostModel.query.all()
    # return render_template('cms/cms_posts.html', posts=post_list)

    # 获取当前页码数
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.MANAGE_PER_PAGE
    end = start + config.MANAGE_PER_PAGE

    query_obj = CommentModel.query.order_by(CommentModel.create_time.desc())
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, per_page=config.MANAGE_PER_PAGE)
    comments = query_obj.slice(start, end)

    context = {
        'comments': comments,
        'pagination': pagination,
    }
    return render_template('pcenter/pc_comments.html', **context)


@bp.route('/dcomments/',methods=['POST'])
@login_required
@permission_required(Permission.POSTER)
def dcomments():
    comment_id = request.form.get("comment_id")
    if not comment_id:
        return restful.params_error('请传入评论id!')
    comment = CommentModel.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return restful.success(message='deleted!')
    else:
        return restful.params_error(message='没有这个评论')

@bp.route('/users/')
@login_required
@permission_required(Permission.USER)
def users():
    # post_list = PostModel.query.all()
    # return render_template('cms/cms_posts.html', posts=post_list)

    # 获取当前页码数
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.MANAGE_PER_PAGE
    end = start + config.MANAGE_PER_PAGE

    query_obj = User.query.order_by(User.join_time.desc())
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, per_page=config.MANAGE_PER_PAGE)
    users = query_obj.slice(start, end)

    context = {
        'users': users,
        'pagination': pagination,
    }
    return render_template('pcenter/pc_users.html', **context)

@bp.route('/muser/',methods=['POST'])
@login_required
@permission_required(Permission.USER)
def muser():
    user_id = request.form.get("user_id")
    if not user_id:
        return restful.params_error('请传入用户id!')
    user = User.query.get(user_id)
    if user:
        user.roles = []
        db.session.commit()
        role = Role.query.filter_by(name='访问者').first()
        if role:
            role.users.append(user)
            db.session.commit()

        return restful.success()
    else:
        return restful.params_error("没有这个用户！")


@bp.route('/umuser/',methods=['POST'])
@login_required
@permission_required(Permission.USER)
def umuser():
    user_id = request.form.get("user_id")
    if not user_id:
        return restful.params_error('请传入用户id!')
    user = User.query.get(user_id)
    if user:
        user.roles = []
        db.session.commit()

        role = Role.query.filter_by(name='运营').first()
        if role:
            role.users.append(user)
            db.session.commit()

        return restful.success()
    else:
        return restful.params_error("没有这个用户！")


class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('pcenter/pc_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.front_user

            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误")

        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'), strict_slashes=False)
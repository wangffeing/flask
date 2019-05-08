from flask import Blueprint, views, render_template, request, make_response
from flask import session, url_for, g, abort, redirect
from utils import safeutils, restful
from ..models import User, BoardModel, PostModel, BannerModel, CommentModel, HighlightPostModel, VotePostUserModel
from .forms import SigninForm, AddPostForm, AddCommentForm
from  ..decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from exts import db
import config

from sqlalchemy import func, and_
from typing import Any, Union

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    board_id = request.args.get('bd', type=int, default=None)

    # 页码
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE

    sort = request.args.get('st', type=int, default=1)
    query_obj = None

    #  时间排序
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    #  精华排序
    elif sort == 2:
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    #  点赞排序
    elif sort == 3:
        query_obj = db.session.query(PostModel).outerjoin(VotePostUserModel).group_by(PostModel.id).order_by(func.count(VotePostUserModel.id).desc(), PostModel.create_time.desc())
    #  评论数量排序
    elif sort == 4:
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)

    posts = query_obj.slice(start, end)
    total = query_obj.count()

    # bs_version=3:表示用Bootstrap v3版本
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)

    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort,
    }

    return render_template('front/front_index.html', **context)


@bp.route('/search/<keywords>/')
def search(keywords):
    """ Search the topic which contains all the keywords in title or content.

    Refer to:
    Object Relational Tutorial
    http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#common-filter-operators
    query.filter(User.name.like('%ed%'))
    query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
    query.filter(or_(User.name == 'ed', User.name == 'wendy'))
    """
    keys = keywords.split(' ')
    all_topics = (PostModel.query.filter(
        and_(*[PostModel.title_content.like("%" + k + "%") for k in keys])).all())

    # print("AAA", all_topics[0].topic_deleted, all_topics[0].deleted)
    all_topics.sort(key=lambda x: x.create_time, reverse=True)

    per_page = config.PER_PAGE

    page = int(request.args.get('page', 1))
    offset = (page - 1) * per_page
    topics = all_topics[offset:offset + per_page]

    # bs_version=3:表示用Bootstrap v3版本

    pagination = Pagination(page=page, total=len(all_topics),
                            per_page=per_page,
                            record_name="topic",
                            CSS_FRAMEWORK='bootstrap',
                            bs_version=3)

    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)

    boards = BoardModel.query.all()
    board_id = request.args.get('bd', type=int, default=None)
    sort = request.args.get("st", type=int, default=1)

    context = {
        'banners': banners,
        'boards': boards,
        'posts': topics,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort,
    }
    return render_template('front/front_index.html', **context)

@bp.route('/apost/', methods=['POST', 'GET'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个版块')
            post = PostModel(title=title, content=content, board_id=board_id)
            post.author = g.user
            post.board = board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    post.read_count = post.read_count + 1
    db.session.add(post)
    db.session.commit()
    return render_template('front/front_pdetail.html', post=post)

@bp.route('/acomment/', methods=['POST'])
@login_required
def add_comment():
    add_comment_form = AddCommentForm(request.form)
    x = add_comment_form.validate()
    if add_comment_form.validate():
        content = add_comment_form.content.data
        post_id = add_comment_form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个帖子')
    else:
        return restful.params_error(add_comment_form.get_error())

@bp.route('/avote/',methods=['POST'])
@login_required
def avote():
    post_id = request.form.get('post_id')
    post = PostModel.query.get(post_id)
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id!')
    if not post:
        return restful.params_error("没有这篇帖子！")

    vote = VotePostUserModel()
    vote.postv = post
    vote.userv = g.user

    db.session.add(vote)
    db.session.commit()

    return restful.success()

@bp.route('/logout/')
@login_required
def logout():
    del session[config.USER_ID]
    return redirect(url_for('front.signin'))

class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url  and safeutils.is_safe_url(
                return_to):
            return render_template('front/signin.html', return_to=return_to)
        else:
            return render_template('front/signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            zxbh = form.zxbh.data
            password = form.password.data
            remember = form.remember.data
            user = User.query.filter_by(zxbh=zxbh).first()
            if user and user.check_password(password):
                session[config.USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='在线编号或密码错误')
        else:
            return restful.params_error(message=form.get_error())

bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))